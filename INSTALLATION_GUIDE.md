# WebLock - Complete Installation Guide for Local Laptop

## 📋 System Requirements

### Supported Operating Systems
- ✅ Windows 10/11
- ✅ macOS (Intel or Apple Silicon)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning)
- 2GB RAM minimum
- 500MB free disk space

---

## 🚀 Installation Steps

### Step 1: Install Python

#### Windows
1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Verify installation:
```cmd
python --version
pip --version
```

#### macOS
```bash
# Using Homebrew
brew install python3

# Verify
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

---

### Step 2: Download WebLock

#### Option A: Download ZIP
1. Download the WebLock project folder
2. Extract to desired location (e.g., `C:\WebLock` or `~/WebLock`)
3. Open terminal/command prompt in that folder

#### Option B: Using Git (if available)
```bash
# Navigate to where you want the project
cd Desktop

# Clone or copy the project
# (Assuming you have the files)
```

---

### Step 3: Navigate to Project Directory

```bash
# Windows Command Prompt
cd C:\path\to\weblock

# macOS/Linux Terminal
cd ~/path/to/weblock

# Verify you're in the right directory
dir    # Windows
ls     # macOS/Linux
```

You should see files like:
- `app.py`
- `trap.py`
- `requirements.txt`
- `config.json`
- `templates/` folder
- `static/` folder

---

### Step 4: Create Virtual Environment (Recommended)

#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal prompt when activated.

---

### Step 5: Install Dependencies

```bash
# Make sure you're in the project directory with (venv) active
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- pymongo (database)
- pandas (data processing)
- fpdf (PDF reports)
- requests (API calls)
- psutil (system info)

**Note:** Optional dependencies (opencv-python, PyAutoGUI, pynput) are NOT required for DEMO_MODE.

---

### Step 6: Verify Installation

Check if all required files exist:

```bash
# Windows
dir templates
dir static
dir model

# macOS/Linux
ls templates/
ls static/
ls model/
```

You should see:
- **templates/** - 6 HTML files
- **static/** - css, js, images folders
- **model/** - data.json, students.json, admin_settings.json

---

### Step 7: Run WebLock

```bash
python app.py
```

You should see:
```
============================================================
🔐 WebLock - Intrusion Detection System
============================================================
📝 DEMO MODE: True
🌐 Access the application at: http://localhost:5000
============================================================
 * Running on http://127.0.0.1:5000
```

---

## 🌐 Access the Application

### Open in Browser
1. Open your web browser (Chrome, Firefox, Edge, Safari)
2. Go to: **http://localhost:5000**
3. You should see the WebLock login page

### Test Credentials

**Student Login:**
```
Email: 2211cs040100@mru.edu.in
Password: Student@100
```

**Admin Login:**
```
Username: admin
Password: Admin@123
```

**Honeypot Test (Triggers Trap):**
```
Username: root
Password: toor
```

---

## 🛠️ Troubleshooting

### Problem: "Python not found"
**Solution:**
```bash
# Try python3 instead
python3 --version
python3 app.py
```

### Problem: "pip not found"
**Solution:**
```bash
# Windows
python -m pip install -r requirements.txt

# macOS/Linux
python3 -m pip install -r requirements.txt
```

### Problem: "Address already in use (Port 5000)"
**Solution:**
```bash
# Something is using port 5000
# Option 1: Find and stop that process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Option 2: Change port in app.py (bottom of file)
# Change: app.run(host='0.0.0.0', port=5000, debug=True)
# To: app.run(host='0.0.0.0', port=8000, debug=True)
```

### Problem: "Module not found" errors
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If specific module fails
pip install flask
pip install pymongo
pip install pandas
```

### Problem: "Permission denied"
**Solution (Windows):**
- Run Command Prompt as Administrator
- Disable antivirus temporarily during installation

**Solution (macOS/Linux):**
```bash
sudo python3 app.py
# Or fix permissions
chmod +x app.py
```

### Problem: MongoDB Connection Failed
**Solution:**
This is **normal**! The system runs in DEMO_MODE without MongoDB.
- All data is stored in JSON/CSV files
- You'll see: `⚠️ MongoDB not available` - **This is okay!**
- System works perfectly with file-based storage

---

## 📂 Project Structure

```
weblock/
├── app.py                    # Main Flask application
├── trap.py                   # Trap functions (7 core functions)
├── database.py               # Database operations
├── config.json              # Configuration
├── requirements.txt         # Python dependencies
│
├── templates/               # HTML templates
│   ├── login.html
│   ├── fake_admin.html
│   ├── student_dashboard.html
│   ├── student_profile.html
│   ├── student_academics.html
│   └── admin_dashboard.html
│
├── static/                  # Frontend assets
│   ├── css/
│   │   ├── style.css
│   │   └── student.css
│   ├── js/
│   │   └── loading.js
│   └── images/
│       └── mru_logo.png
│
├── model/                   # Data files
│   ├── data.json           # Student data
│   ├── students.json
│   └── admin_settings.json
│
├── logs/                    # Runtime logs
│   ├── intrusions.json
│   ├── intruder_log.csv
│   └── key_logs.json
│
└── Capture/                 # Forensic evidence
    ├── intruder/           # Webcam photos
    └── screenshots/        # Screenshots
```

---

## 🎯 Quick Start Commands

### Starting the Server
```bash
# Make sure virtual environment is active
python app.py

# OR if python3 is your command
python3 app.py
```

### Stopping the Server
- Press `Ctrl + C` in the terminal
- Or close the terminal window

### Restarting the Server
1. Stop with `Ctrl + C`
2. Run `python app.py` again

---

## 🔧 Configuration

### Change Port Number
Edit `app.py` (last line):
```python
# Default
app.run(host='0.0.0.0', port=5000, debug=True)

# Change to port 8000
app.run(host='0.0.0.0', port=8000, debug=True)
```

### Enable/Disable Debug Mode
Edit `app.py`:
```python
# Debug ON (shows detailed errors)
app.run(debug=True)

# Debug OFF (production mode)
app.run(debug=False)
```

### Modify DEMO_MODE
Edit `config.json`:
```json
{
    "demo_mode": true,     // Change to false for real captures
    "consent_required": true
}
```

**Warning:** Setting `demo_mode: false` requires:
- Webcam access
- opencv-python installed
- PyAutoGUI installed
- pynput installed

---

## 📱 Accessing from Other Devices

### On Same Network

1. Find your laptop's IP address:

**Windows:**
```cmd
ipconfig
# Look for "IPv4 Address" under your WiFi adapter
# Example: 192.168.1.100
```

**macOS:**
```bash
ifconfig | grep "inet "
# Look for IP like 192.168.1.100
```

**Linux:**
```bash
ip addr show
# Or
hostname -I
```

2. Make sure firewall allows port 5000

3. On your phone/other device, open browser and go to:
```
http://YOUR_IP:5000
Example: http://192.168.1.100:5000
```

---

## 🎓 Demo Workflow

### For University Presentation

**1. Start the Server**
```bash
cd weblock
python app.py
```

**2. Show Login Page**
- Open http://localhost:5000
- Highlight clean mobile 9:16 design
- Show India Standard Time in status bar

**3. Demonstrate Student Access**
```
Login: 2211cs040100@mru.edu.in / Student@100
→ Show dashboard
→ Navigate to Profile
→ View Academics
→ Logout
```

**4. Trigger Honeypot**
```
Login: root / toor
→ Trap activates (check terminal logs)
→ Redirects to fake admin (mobile 9:16)
→ Click buttons to show toast notifications
→ Logout
```

**5. Show Admin Dashboard**
```
Login: admin / Admin@123
→ View captured intrusion
→ Show statistics
→ Export data
→ View forensic evidence
```

**6. SQL Injection Demo**
```
Login: admin'--@test.com / admin' OR 'x'='x
→ Trap triggers
→ Show detection in admin dashboard
```

---

## 🔒 Security Notes

### For Demonstrations Only
- This is an **educational project**
- Not intended for production security
- All traps are logged for forensic analysis
- DEMO_MODE uses sample data (no real captures)

### Privacy
- DEMO_MODE: Safe for presentations
- No real webcam/screenshot capture
- No actual keystroke logging
- Sample data used for evidence

---

## 📊 Viewing Captured Data

### Intrusion Logs
```bash
# View JSON format
notepad logs/intrusions.json          # Windows
cat logs/intrusions.json              # macOS/Linux

# View CSV format
notepad logs/intruder_log.csv         # Windows
cat logs/intruder_log.csv             # macOS/Linux
```

### Captured Photos (DEMO MODE)
```bash
# Navigate to captures
cd Capture/intruder/
dir              # Windows
ls -la           # macOS/Linux
```

---

## 🆘 Getting Help

### Common Issues

**1. Browser can't connect**
- Check if server is running (look for Flask output in terminal)
- Try http://127.0.0.1:5000 instead
- Clear browser cache

**2. Pages look broken**
- Clear browser cache (Ctrl+Shift+Del)
- Hard refresh (Ctrl+F5 or Cmd+Shift+R)
- Check if static files exist

**3. Login doesn't work**
- Check credentials are exact (case-sensitive)
- Check terminal for error messages
- Verify data.json and admin_settings.json exist

**4. Time not updating**
- Check JavaScript console (F12 in browser)
- Ensure JavaScript is enabled
- Try different browser

---

## ✅ Verification Checklist

Before presenting, verify:

- [ ] Python installed and working
- [ ] All dependencies installed
- [ ] Server starts without errors
- [ ] Login page loads with IST time
- [ ] Student login works
- [ ] Admin login works
- [ ] Honeypot triggers trap
- [ ] Fake admin shows toast notifications
- [ ] All buttons functional
- [ ] 9:16 mobile design works
- [ ] Icons fit properly
- [ ] Data exports work

---

## 🎉 You're Ready!

Your WebLock system is now installed and running on your laptop!

**Access:** http://localhost:5000

**Features Working:**
- ✅ India Standard Time display
- ✅ 9:16 Mobile application design
- ✅ All trap functions operational
- ✅ Student portal with full profiles
- ✅ Honeypot with working buttons
- ✅ Admin dashboard with forensics
- ✅ Data export (JSON/CSV)

**Quick Test:**
1. Open http://localhost:5000
2. See current IST time
3. Login with `admin` / `Admin@123`
4. System is ready! 🎊

---

## 📞 Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Verify all files are present
3. Ensure Python version is 3.10+
4. Try reinstalling dependencies

**Last Updated:** November 25, 2025  
**Project Name:** WebLock  
**Version:** 2.1 - Local Installation Ready
