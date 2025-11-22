import os
import numpy as np
import cv2
from PIL import Image

# GPU Configuration
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF warnings

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    
    # Enable GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"✓ GPU detected and enabled: {len(gpus)} GPU(s)")
        except RuntimeError as e:
            print(f"GPU configuration error: {e}")
    else:
        print("No GPU detected - will use CPU")
        
except ImportError:
    import keras
    from keras import layers
    print("Using Keras without TensorFlow GPU support")
    
import json

class AutismDetector:
    """
    AI model for detecting potential autism in children through facial expression analysis
    """
    
    def __init__(self, model_path=None):
        self.model = None
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        self.model_path = model_path or os.path.join(os.path.dirname(__file__), 'autism_model.h5')
        
        # Load or create model
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.create_model()
    
    def create_model(self):
        """Create a model for autism detection using Transfer Learning (MobileNetV2)"""
        try:
            base_model = tf.keras.applications.MobileNetV2(
                input_shape=(224, 224, 3),
                include_top=False,
                weights='imagenet'
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            self.model = keras.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.5),
                layers.Dense(64, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(1, activation='sigmoid')
            ])
            
            self.model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            print("Created MobileNetV2 based model")
            
        except Exception as e:
            print(f"Error creating MobileNetV2 model: {e}")
            print("Falling back to simple CNN")
            # Fallback to simple CNN if MobileNetV2 fails (e.g. no internet for weights)
            self._create_simple_cnn()

    def _create_simple_cnn(self):
        """Fallback simple CNN"""
        self.model = keras.Sequential([
            layers.Input(shape=(224, 224, 3)),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
    
    def load_model(self):
        """Load pre-trained model"""
        try:
            self.model = keras.models.load_model(self.model_path)
            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Could not load model: {e}. Creating new model.")
            self.create_model()
    
    def save_model(self):
        """Save trained model"""
        if self.model:
            self.model.save(self.model_path)
            print(f"Model saved to {self.model_path}")
    
    def preprocess_image(self, image_array):
        """Preprocess image for model input"""
        # Convert to RGB if grayscale
        if len(image_array.shape) == 2:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
        elif image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        # Resize to model input size
        image_resized = cv2.resize(image_array, (224, 224))
        
        # Preprocess for MobileNetV2 (expects values in [-1, 1])
        # tf.keras.applications.mobilenet_v2.preprocess_input does this
        # But to avoid dependency on tf in this method if possible, we can do it manually
        # MobileNetV2 preprocessing: (x / 127.5) - 1
        image_normalized = (image_resized.astype('float32') / 127.5) - 1.0
        
        return image_normalized
    
    def detect_faces(self, image_array):
        """Detect faces in the image"""
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces
    
    def detect_eyes(self, image_array, face_region):
        """Detect eyes in a face region"""
        x, y, w, h = face_region
        face_roi = image_array[y:y+h, x:x+w]
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray_face)
        return eyes
    
    def extract_facial_features(self, image_array, faces):
        """Extract facial features from detected faces"""
        features = {
            'face_count': len(faces),
            'eye_contact': 0.5,  # Default value if no faces detected
            'face_symmetry': 0.5,
            'expression_intensity': 0.5,
            'head_position': 'frontal'
        }
        
        if len(faces) == 0:
            return features
        
        # Analyze primary face
        x, y, w, h = faces[0]
        
        # Ensure valid coordinates
        y_start = max(0, y)
        y_end = min(image_array.shape[0], y + h)
        x_start = max(0, x)
        x_end = min(image_array.shape[1], x + w)
        
        if y_end <= y_start or x_end <= x_start:
            return features
        
        face_roi = image_array[y_start:y_end, x_start:x_end]
        
        if face_roi.size == 0:
            return features
        
        # Eye detection and contact analysis
        eyes = self.detect_eyes(image_array, faces[0])
        eye_contact_score = min(1.0, len(eyes) / 2.0)  # 0.0 to 1.0
        features['eye_contact'] = float(eye_contact_score)
        
        # Face symmetry analysis
        try:
            symmetry = self.analyze_symmetry(face_roi)
            features['face_symmetry'] = float(symmetry)
        except:
            features['face_symmetry'] = 0.5
        
        # Expression intensity
        try:
            expression = self.analyze_expression(face_roi)
            features['expression_intensity'] = float(expression)
        except:
            features['expression_intensity'] = 0.5
        
        # Face size relative to image
        face_area = (w * h) / (image_array.shape[0] * image_array.shape[1])
        features['face_area_ratio'] = float(face_area)
        
        return features
    
    def analyze_symmetry(self, face_roi):
        """Analyze facial symmetry"""
        gray = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
        h, w = gray.shape
        
        # Split face in half
        left_half = gray[:, :w//2]
        right_half = gray[:, w//2:]
        right_half_flipped = cv2.flip(right_half, 1)
        
        # Calculate symmetry score
        difference = cv2.absdiff(left_half, right_half_flipped)
        symmetry_score = 1 - (np.mean(difference) / 255.0)
        
        return float(max(0, min(1, symmetry_score)))
    
    def analyze_expression(self, face_roi):
        """Analyze expression intensity using edge detection"""
        try:
            gray = cv2.cvtColor(face_roi, cv2.COLOR_RGB2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Expression intensity as percentage of edge pixels
            edge_pixels = np.sum(edges > 0)
            total_pixels = edges.shape[0] * edges.shape[1]
            intensity = edge_pixels / total_pixels
            
            # Scale to 0-1 range more meaningfully (typically 0.05-0.3)
            # Map it so typical expressions give 0.3-0.7 range
            scaled_intensity = min(1.0, max(0.0, intensity * 3.0))
            
            return float(scaled_intensity)
        except:
            return 0.5
    
    def predict(self, image_array):
        """
        Predict autism probability from image
        
        Args:
            image_array: numpy array of image (RGB)
        
        Returns:
            dict with prediction results
        """
        try:
            # Detect faces
            faces = self.detect_faces(image_array)
            
            # Extract facial features
            features = self.extract_facial_features(image_array, faces)
            
            # Preprocess image for model
            processed_image = self.preprocess_image(image_array)
            processed_image = np.expand_dims(processed_image, axis=0)
            
            # Make prediction
            prediction = self.model.predict(processed_image, verbose=0)[0][0]
            
            # Calculate confidence (distance from 0.5)
            confidence = abs(prediction - 0.5) * 2
            
            # Determine status based on prediction and features
            if prediction > 0.7:
                status = "positive"
                recommendations = self.get_positive_recommendations(features)
            elif prediction > 0.4:
                status = "inconclusive"
                recommendations = self.get_inconclusive_recommendations(features)
            else:
                status = "negative"
                recommendations = self.get_negative_recommendations()
            
            return {
                'score': float(prediction),
                'status': status,
                'confidence': float(confidence),
                'features': features,
                'recommendations': recommendations
            }
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {
                'score': 0.0,
                'status': 'error',
                'confidence': 0.0,
                'features': {},
                'recommendations': [f"Error during analysis: {str(e)}"]
            }
    
    def get_positive_recommendations(self, features):
        """Get recommendations when autism indicators are detected"""
        recommendations = [
            "Based on facial expression analysis, we've detected patterns consistent with autism spectrum characteristics.",
            "We recommend scheduling a professional evaluation with a developmental pediatrician or psychologist.",
            "Early intervention services can significantly help. Contact your local early intervention program.",
            "Consider therapies such as ABA (Applied Behavior Analysis), speech therapy, or occupational therapy.",
            "Keep detailed records of your observations to share with healthcare providers.",
            "Build a support network with other parents and professionals.",
            "Remember: This is an initial screening tool, not a diagnosis. Professional assessment is essential."
        ]
        
        if features.get('eye_contact', 0) < 0.3:
            recommendations.append("Work on eye contact through play-based activities and structured practices.")
        
        if features.get('expression_intensity', 0) < 0.15:
            recommendations.append("Limited facial expression intensity detected. Encourage emotional expression through mirroring and social games.")
        
        return recommendations
    
    def get_inconclusive_recommendations(self, features):
        """Get recommendations when results are inconclusive"""
        recommendations = [
            "The analysis shows mixed indicators. We recommend retesting after 2-4 weeks.",
            "Consider taking multiple photos in different lighting and settings for better accuracy.",
            "Consult with a professional for a comprehensive developmental evaluation.",
            "Continue monitoring your child's social interactions and developmental milestones.",
            "Keep a detailed log of behaviors and interactions you observe."
        ]
        return recommendations
    
    def get_negative_recommendations(self):
        """Get recommendations when no autism indicators are detected"""
        recommendations = [
            "Based on facial expression analysis, no significant autism indicators were detected at this time.",
            "Continue regular developmental check-ups with your pediatrician.",
            "Monitor for any developmental changes or new concerns.",
            "Maintain regular social interactions and developmental activities.",
            "If you have any concerns about development, always consult with a professional."
        ]
        return recommendations
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32):
        """Train the model on data"""
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        self.save_model()
        return history
