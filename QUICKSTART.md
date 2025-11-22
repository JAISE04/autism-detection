python app.py# Quick Start Guide

## Installation Steps

### 1. Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

Server runs on: `http://localhost:5000`

### 2. Frontend Setup (New Terminal/Command Window)

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

Frontend opens automatically at: `http://localhost:3000`

## Usage

### First Time Users

1. **Visit Homepage** (`http://localhost:3000`)

   - Read about autism and the platform
   - See how the system works

2. **Try Quick Analysis** (No account needed)

   - Click "Analyze" button
   - Upload a photo of a child's face
   - Get instant analysis results

3. **Create Account** (To save results)

   - Click "Register"
   - Fill in your details
   - Password must be secure

4. **Add Child Profile**

   - From dashboard, click "Add Child"
   - Enter child's name, age, gender
   - Track multiple children

5. **Save Assessments**

   - After analysis, click "Save Assessment"
   - Select or create child profile
   - Results are saved and tracked

6. **Use Chatbot**
   - Navigate to "Chat" page
   - Ask questions about autism
   - Get AI-powered guidance

## Common Issues & Solutions

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`

```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: Port 5000 already in use

```bash
# Solution: Kill process or use different port
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Change port in app.py:
# Change: app.run(debug=True, host='0.0.0.0', port=5000)
# To: app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Issues

**Issue**: `npm: command not found`

```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Issue**: Module not found errors

```bash
# Solution: Clean install
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Port 3000 already in use

```bash
# Solution: Kill process or use different port
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or set custom port:
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # macOS/Linux
```

### Database Issues

**Issue**: Database locked error

```bash
# Solution: Delete old database and restart
rm backend/autism_detection.db
```

## Configuration

### Backend Configuration (app.py)

```python
# Change JWT secret (DO THIS IN PRODUCTION!)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'

# Change database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///autism_detection.db'

# Adjust token expiration
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
```

### Frontend Configuration

Edit `frontend/src/App.js` to change API endpoint:

```javascript
// Change from:
const API_URL = "http://localhost:5000";
// To:
const API_URL = "http://your-api-url";
```

## API Testing

### Using curl or Postman

**Register User**:

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "phone": "1234567890"
  }'
```

**Login**:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Analyze Image**:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "image=@path/to/image.jpg"
```

## Test Data

### Sample Test Credentials

Email: `test@example.com`
Password: `password123`
Name: Test Parent

## Production Deployment

### Backend Deployment (Heroku)

```bash
cd backend

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.9.0" > runtime.txt

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
heroku create your-app-name
heroku config:set JWT_SECRET_KEY=your-secret-key
git push heroku main
```

### Frontend Deployment (Vercel/Netlify)

```bash
cd frontend

# Update API endpoint in App.js
# Then deploy:

# Using Vercel:
npm install -g vercel
vercel

# Or using Netlify:
npm run build
# Upload 'build' folder to Netlify
```

## Next Steps

1. Train the ML model with real autism dataset
2. Set up HTTPS/SSL for production
3. Configure proper database (PostgreSQL for production)
4. Set up email notifications
5. Implement two-factor authentication
6. Add professional consultation booking
7. Set up backup and recovery system

## Support

For issues or questions:

- Check README.md for full documentation
- Review error logs in terminal
- Ensure all ports are available
- Verify all dependencies are installed

---

**Happy using the Autism Detection Platform! 🧠**
