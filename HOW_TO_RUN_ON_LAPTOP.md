# 🚀 How to Run WebLock on Your Laptop

## Quick 3-Step Guide

### Step 1: Install Python
Download and install Python 3.10 or higher from https://www.python.org/downloads/

**Windows:** Make sure to check "Add Python to PATH" during installation!

Verify installation:
```bash
python --version
```

---

### Step 2: Install Dependencies
Open terminal/command prompt in the WebLock folder and run:
```bash
pip install -r requirements.txt
```

---

### Step 3: Run WebLock
```bash
python app.py
```

You'll see:
```
🔐 WebLock - Intrusion Detection System
🌐 Access the application at: http://localhost:5000
```

---

## Open in Browser

Go to: **http://localhost:5000**

You'll see the login page with:
- ✅ India Standard Time (IST) in status bar
- ✅ Clean 9:16 mobile design
- ✅ MRU logo

---

## Test Login Credentials

### Real Admin (Forensic Dashboard)
```
Username: admin
Password: Admin@123
```

### Students
```
Email: 2211cs040100@mru.edu.in
Password: Student@100
```

### Honeypot Test (Triggers Trap)
```
Username: root
Password: toor
```

---

## 🛠️ Troubleshooting

### Python not found?
Try:
```bash
python3 --version
python3 app.py
```

### Port 5000 already in use?
Kill the process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <number> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Module not found errors?
Reinstall:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ✅ Quick Test

1. **Start:** Run `python app.py`
2. **Open:** http://localhost:5000
3. **Login:** `admin` / `Admin@123`
4. **Success!** You should see the admin dashboard

---

## 📱 Features to Test

### Login Page
- ✅ Shows India Standard Time
- ✅ Clean mobile 9:16 design
- ✅ No extra text

### Fake Admin (Honeypot)
Login with `root` / `toor`
- ✅ 9:16 mobile app design
- ✅ All buttons show toast notifications
- ✅ Logout button works

### Student Portal
Login with student credentials
- ✅ Dashboard with profile cards
- ✅ Profile page
- ✅ Academics page
- ✅ All navigation working

### Admin Dashboard
Login with `admin` / `Admin@123`
- ✅ View intrusion incidents
- ✅ Export data (JSON/CSV)
- ✅ Forensic analysis

---

## 🎯 System Files

Make sure these files exist in your WebLock folder:
- ✅ `app.py` - Main application
- ✅ `trap.py` - Trap functions
- ✅ `requirements.txt` - Dependencies
- ✅ `templates/` - HTML files
- ✅ `static/` - CSS, JS, images
- ✅ `model/` - Student data

---

## 🌐 Access from Phone

1. Find your laptop's IP:
```bash
# Windows
ipconfig

# Mac
ifconfig | grep "inet "

# Linux
hostname -I
```

2. On phone browser: `http://YOUR_IP:5000`

Example: `http://192.168.1.100:5000`

---

## 🎓 For Demo/Presentation

1. Start server: `python app.py`
2. Open: http://localhost:5000
3. Show IST time in status bar
4. Demonstrate:
   - Clean login page
   - Student portal (mobile 9:16)
   - Honeypot (fake admin with working buttons)
   - Admin dashboard (forensic data)
   - SQL injection detection

---

## ⚠️ Important Notes

### MongoDB Warning is Normal!
You'll see:
```
⚠️ MongoDB not available
```
**This is okay!** The system works perfectly without MongoDB using file-based storage.

### DEMO MODE is Active
- No real webcam capture (uses sample image)
- No actual keylogging (simulated data)
- Safe for demonstrations!

---

## 🎉 You're Ready!

**Project Name:** WebLock  
**Access:** http://localhost:5000  
**Admin Login:** admin / Admin@123

All features working:
- ✅ India Standard Time
- ✅ 9:16 mobile design
- ✅ All buttons functional
- ✅ Trap system operational
- ✅ Admin dashboard ready

**Ready for demonstration!** 🎊

---

For detailed installation instructions, see **INSTALLATION_GUIDE.md**
