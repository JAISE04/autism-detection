import os
import sys
import json
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
import io
import base64

# Add parent directory to path so we can import ml_model
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_model.autism_detector import AutismDetector

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autism_detection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Initialize ML model
autism_detector = AutismDetector()

# ============== DATABASE MODELS ==============

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    children = db.relationship('Child', backref='parent', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    assessments = db.relationship('Assessment', backref='child', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('Note', backref='child', lazy=True, cascade='all, delete-orphan')

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    autism_score = db.Column(db.Float)  # Probability score
    facial_features = db.Column(db.Text)  # JSON string
    status = db.Column(db.String(20))  # 'positive', 'negative', 'inconclusive'
    image_path = db.Column(db.String(500))
    recommendations = db.Column(db.Text)  # JSON string

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    note_type = db.Column(db.String(50))  # 'observation', 'milestone', 'concern'
    content = db.Column(db.Text)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('User', backref='chat_messages')

# ============== AUTHENTICATION ROUTES ==============

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password') or not data.get('full_name'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=data['email'],
            full_name=data['full_name'],
            phone=data.get('phone', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Registration successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'phone': user.phone,
            'children_count': len(user.children)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== ANALYSIS ROUTES ==============

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read and process image
        image = Image.open(file.stream).convert('RGB')
        image_array = np.array(image)
        
        # Detect faces and analyze
        result = autism_detector.predict(image_array)
        
        return jsonify({
            'success': True,
            'autism_score': float(result['score']),
            'status': result['status'],
            'facial_features': result['features'],
            'recommendations': result['recommendations'],
            'confidence': float(result['confidence'])
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== CHILD PROFILE ROUTES ==============

@app.route('/api/children', methods=['POST'])
@jwt_required()
def add_child():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Child name is required'}), 400
        
        child = Child(
            parent_id=user_id,
            name=data['name'],
            age=data.get('age'),
            gender=data.get('gender')
        )
        
        db.session.add(child)
        db.session.commit()
        
        return jsonify({
            'message': 'Child profile created',
            'child': {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/children', methods=['GET'])
@jwt_required()
def get_children():
    try:
        user_id = get_jwt_identity()
        children = Child.query.filter_by(parent_id=user_id).all()
        
        return jsonify({
            'children': [{
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender,
                'assessments_count': len(child.assessments)
            } for child in children]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/children/<int:child_id>', methods=['GET'])
@jwt_required()
def get_child_details(child_id):
    try:
        user_id = get_jwt_identity()
        child = Child.query.filter_by(id=child_id, parent_id=user_id).first()
        
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        
        assessments = [{
            'id': a.id,
            'date': a.assessment_date.isoformat(),
            'score': a.autism_score,
            'status': a.status,
            'recommendations': json.loads(a.recommendations) if a.recommendations else []
        } for a in child.assessments]
        
        notes = [{
            'id': n.id,
            'date': n.created_at.isoformat(),
            'type': n.note_type,
            'content': n.content
        } for n in child.notes]
        
        return jsonify({
            'child': {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender
            },
            'assessments': assessments,
            'notes': notes
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== ASSESSMENT ROUTES ==============

@app.route('/api/assessment/save', methods=['POST'])
@jwt_required()
def save_assessment():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('child_id'):
            return jsonify({'error': 'Child ID is required'}), 400
        
        child = Child.query.filter_by(id=data['child_id'], parent_id=user_id).first()
        
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        
        assessment = Assessment(
            child_id=child.id,
            autism_score=data.get('autism_score'),
            facial_features=json.dumps(data.get('facial_features', {})),
            status=data.get('status'),
            image_path=data.get('image_path'),
            recommendations=json.dumps(data.get('recommendations', []))
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'message': 'Assessment saved successfully',
            'assessment_id': assessment.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/<int:child_id>', methods=['GET'])
@jwt_required()
def get_assessments(child_id):
    try:
        user_id = get_jwt_identity()
        child = Child.query.filter_by(id=child_id, parent_id=user_id).first()
        
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        
        assessments = Assessment.query.filter_by(child_id=child_id).all()
        
        return jsonify({
            'assessments': [{
                'id': a.id,
                'date': a.assessment_date.isoformat(),
                'score': a.autism_score,
                'status': a.status,
                'facial_features': json.loads(a.facial_features) if a.facial_features else {},
                'recommendations': json.loads(a.recommendations) if a.recommendations else []
            } for a in assessments]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== CHATBOT ROUTES ==============

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        
        # Simple chatbot response logic
        chatbot_response = generate_chatbot_response(user_message)
        
        # Save chat message
        chat_msg = ChatMessage(
            user_id=user_id,
            message=user_message,
            response=chatbot_response
        )
        
        db.session.add(chat_msg)
        db.session.commit()
        
        return jsonify({
            'message': user_message,
            'response': chatbot_response,
            'timestamp': chat_msg.created_at.isoformat()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    try:
        user_id = get_jwt_identity()
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at).all()
        
        return jsonify({
            'messages': [{
                'id': m.id,
                'message': m.message,
                'response': m.response,
                'timestamp': m.created_at.isoformat()
            } for m in messages]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== HELPER FUNCTIONS ==============

def generate_chatbot_response(user_message):
    """Generate chatbot response based on user message"""
    
    message_lower = user_message.lower()
    
    # Autism information responses
    if 'autism' in message_lower and 'what is' in message_lower:
        return "Autism Spectrum Disorder (ASD) is a developmental condition characterized by differences in social communication, interaction, and behavior. Early identification and intervention can significantly improve outcomes. Our system helps detect potential signs through facial expression analysis."
    
    elif 'sign' in message_lower and ('autism' in message_lower or 'asd' in message_lower):
        return "Common early signs of autism include: limited eye contact, challenges with social interaction, repetitive behaviors, sensory sensitivities, and differences in facial expression patterns. If you notice these in your child, consider a professional evaluation."
    
    elif 'early' in message_lower and 'intervention' in message_lower:
        return "Early intervention is crucial for children with autism. Therapies like ABA (Applied Behavior Analysis), speech therapy, and occupational therapy can help develop skills. The earlier intervention starts, the better the outcomes."
    
    elif 'facial' in message_lower and 'expression' in message_lower:
        return "Facial expressions play a key role in social communication. Children with autism may show different patterns in expression recognition and production. Our AI analyzes these patterns to assist in early identification."
    
    elif 'progres' in message_lower and 'track' in message_lower:
        return "You can track your child's progress through regular assessments. Keep detailed notes about observations and milestones. Our platform helps you maintain records and identify patterns over time."
    
    elif 'help' in message_lower or 'support' in message_lower:
        return "We're here to support you. You can: 1) Use our diagnosis tool regularly, 2) Keep detailed notes on observations, 3) Track progress over time, 4) Consult with professionals, and 5) Join support communities. Remember, you're not alone in this journey."
    
    elif 'emergency' in message_lower:
        return "If your child is in immediate distress or danger, please contact emergency services (911 in the US). For crisis support, consider contacting the National Suicide Prevention Lifeline or Autism Speaks."
    
    elif 'school' in message_lower or 'education' in message_lower:
        return "Educational support for children with autism may include IEPs (Individualized Education Programs), classroom accommodations, and specialized services. Work with your school to develop appropriate support plans."
    
    else:
        return "I'm here to help you understand and support your child. I can provide information about autism, early intervention, progress tracking, and coping strategies. What would you like to know more about?"

# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============== MAIN ==============

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
