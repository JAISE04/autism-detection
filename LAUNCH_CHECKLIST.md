# 🚀 Quick Launch Checklist

## Pre-Launch Verification (1 minute)

### System Requirements Check

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 14+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] 5+ GB free disk space
- [ ] Ports 5000 and 3000 available

## Backend Launch (2-3 minutes)

### Step 1: Open Terminal/Command Prompt

```
Navigate to: Autism_detection/backend
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

✅ You should see `(venv)` in your terminal prompt

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

⏱️ This takes 5-10 minutes (first time)

### Step 4: Initialize Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Step 5: Start Server

```bash
python app.py
```

✅ Expected message: `Running on http://127.0.0.1:5000`

**Keep this terminal open!**

## Frontend Launch (2-3 minutes)

### Step 1: Open New Terminal/Command Prompt

```
Navigate to: Autism_detection/frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

⏱️ This takes 3-5 minutes (first time)

### Step 3: Start Development Server

```bash
npm start
```

✅ Expected: Browser opens automatically to `http://localhost:3000`

**Keep this terminal open!**

## Application Ready ✨

### Now You Can:

- 🏠 Visit homepage
- 📸 Upload an image for analysis (no login needed)
- 📝 Create an account
- 👨‍👩‍👧 Add children
- 📊 View dashboard
- 💬 Chat with bot

## Stopping the Application

### To Stop Backend

```
Press CTRL+C in backend terminal
```

### To Stop Frontend

```
Press CTRL+C in frontend terminal
```

## Troubleshooting Quick Fixes

| Problem                           | Quick Fix                                  |
| --------------------------------- | ------------------------------------------ |
| Port already in use               | Kill process on port or use different port |
| Module not found                  | Run `pip install -r requirements.txt`      |
| npm install fails                 | Try `npm cache clean --force` then install |
| Can't connect frontend to backend | Check both servers are running             |
| Page won't load                   | Clear browser cache (Ctrl+Shift+Delete)    |

## Testing Credentials (for development)

You can create any test account, but here's a template:

**Email**: test@example.com  
**Password**: password123  
**Name**: Test Parent

## First Steps in Application

1. **Homepage** - Read about autism detection
2. **Analyze Page** - Upload any child photo to see analysis
3. **Register** - Create your own account
4. **Add Child** - Add a child profile
5. **Dashboard** - View your children
6. **Chat** - Ask questions to the chatbot

## Verify Everything Works

- [ ] Backend running: `http://localhost:5000` accessible
- [ ] Frontend running: `http://localhost:3000` accessible
- [ ] Can upload image and get analysis
- [ ] Can register new account
- [ ] Can add child profile
- [ ] Can see chatbot responses

## Next Steps

After verifying everything works:

1. **Train the ML Model** (optional)

   - See `INSTALLATION.md` for dataset preparation
   - Run `python ml_model/train_model.py`

2. **Deploy to Production**

   - Follow deployment guide in `INSTALLATION.md`
   - Set production environment variables
   - Configure domain and SSL

3. **Customize**
   - Add your branding
   - Configure chatbot responses
   - Update colors and theme

## Useful Links

- 📖 Full Documentation: `README.md`
- ⚡ Quick Start: `QUICKSTART.md`
- 🔧 Installation Help: `INSTALLATION.md`
- 📊 Project Overview: `PROJECT_SUMMARY.md`

## Common Ports

| Service  | Port | URL                   |
| -------- | ---- | --------------------- |
| Frontend | 3000 | http://localhost:3000 |
| Backend  | 5000 | http://localhost:5000 |
| Database | N/A  | SQLite (local file)   |

## Tips

💡 **Pro Tips**:

- Keep both terminals visible for debugging
- Clear browser cache if you see old UI
- Check terminal error messages for specific issues
- Use browser DevTools (F12) for frontend issues
- Check logs in terminal for backend issues

## Estimated Time

| Task               | Time        |
| ------------------ | ----------- |
| Check requirements | 1 min       |
| Backend setup      | 10 min      |
| Frontend setup     | 10 min      |
| **Total**          | **~20 min** |

## Support

If you encounter issues:

1. Check `INSTALLATION.md` troubleshooting section
2. Verify all requirements are installed
3. Check error messages in terminals
4. Ensure ports 3000 and 5000 are free
5. Try clearing npm cache: `npm cache clean --force`

---

## Status Indicators

When everything is working correctly:

✅ Backend Terminal:

```
Running on http://127.0.0.1:5000
WARNING in app.run()...  (this is normal)
```

✅ Frontend Terminal:

```
Compiled successfully!

You can now view autism-detection-frontend in the browser.

Local:            http://localhost:3000
```

✅ Browser:
Shows homepage with:

- Navigation bar at top
- Autism Detection title
- Information sections
- "Get Started" buttons

---

**You're All Set! Happy Coding! 🎉**

If you need help:

- Read the documentation files
- Check the troubleshooting section
- Review error messages in terminals

**Happy using the Autism Detection Platform!** 🧠
