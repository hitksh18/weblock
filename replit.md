# WebLock - Intrusion Detection System

## Overview

WebLock is an educational intrusion detection demonstration system designed for Malla Reddy University. It's a Flask-based web application that simulates a student portal while implementing defensive security mechanisms to detect and track various attack vectors including SQL injection, XSS, brute force attempts, and other malicious activities. The system operates in demo mode by default for safe presentation environments and features both a honeypot trap system and a real admin dashboard for forensic analysis.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Updates (November 25, 2025)

### Real-Time Analytics & AI Pattern Learning System
**Analytics Features:**
- **Live Data Integration** - All charts now fetch real-time data from intrusion logs via `/api/analytics/realtime`
- **Attack Type Distribution** - Doughnut chart showing SQL injection, XSS, brute force, honeypot hits, and device spoofing counts
- **Timeline Analysis** - 7-day trend line chart displaying intrusion patterns over time
- **Geographic Distribution** - Bar chart of top 10 countries by attack count
- **Risk Score Analysis** - Pie chart categorizing attacks as high/medium/low risk

**AI Pattern Learning:**
- **Automatic Learning** - System learns from every detected attack and saves new patterns to `ai_training/<type>.json`
- **External Threat Intelligence** - Integration framework for AbuseIPDB, VirusTotal, AlienVault OTX APIs (simulated for demo)
- **Pattern Normalization** - Attack types mapped to canonical filenames (e.g., "Cross-Site Scripting (XSS)" → "xss.json")
- **Manual Training** - Admin dashboard button to manually trigger AI training from external threat feeds
- **IP Reputation Checking** - `/api/threat-intel/ip/<ip>` endpoint for threat scoring

**AI Performance Dashboard:**
- Pattern count metrics (total: 302 patterns - 109 SQL injection, 183 XSS, 10 payload injection)
- Detection accuracy by attack type
- Average confidence score display (91.67% across all detections)
- High confidence rate tracking (100% of detections above 80% confidence)

**New API Endpoints:**
- `/api/analytics/realtime` - Real-time data for all dashboard charts
- `/api/ai/patterns` - Current AI pattern statistics
- `/api/ai/performance` - Detection accuracy and confidence metrics
- `/api/ai/train` (POST) - Manually trigger AI training from threat intelligence
- `/api/threat-intel/ip/<ip_address>` - Check IP reputation

### Modern Responsive Admin Dashboard - Complete Redesign
**Modern UI Features:**
- **Collapsible Sidebar** - Hamburger menu for mobile/tablet devices (≤1024px)
- **Quick Action Cards** - 6 shortcut cards on dashboard home for fast navigation
- **Responsive Design** - Fully adaptive layout for desktop, tablet, and mobile
- **Modern Visual Effects:**
  - Gradient backgrounds on cards and sidebar
  - Smooth hover animations and transforms
  - Custom orange-themed scrollbar
  - Box shadows and border highlights
  - Smooth scroll behavior
  - Backdrop blur on mobile overlay

**Responsive Breakpoints:**
- **Desktop (>1024px)** - Fixed sidebar, full grid layouts
- **Tablet (≤1024px)** - Collapsible sidebar with hamburger menu
- **Mobile (≤768px)** - Single column layouts, stacked elements
- **Small Mobile (≤480px)** - Optimized touch targets and spacing

**Quick Action Shortcuts:**
1. View Intrusions - Direct access to attack logs
2. Captured Evidence - Forensic images browser
3. Keystroke Logs - Keylog file viewer
4. Analytics - Chart visualizations
5. Attack Map - Geographic attack map
6. Student Data - Student database management

**Evidence Management Enhancement:**
- **Captured Evidence** section with split-view interface (file browser + image preview)
- **Keylogs** section with split-view interface (file list + content viewer)
- Real-time file loading when sections are accessed
- Image preview with metadata (filename, size, type)
- Keylog content viewer with formatted display
- Automatic refresh functionality

**API Endpoints:**
- `/api/captured-files` - Lists images from Capture/intruder and Capture/screenshots directories
- `/api/keylog-files` - Lists keylog JSON files from logs directory
- `/api/keylog-content?file=<path>` - Retrieves keylog file contents
- `/Capture/<path>` - Serves captured images and screenshots

**Student Data Display Fix:**
- Updated template to correctly extract nested JSON data from model/data.json
- Full name from `profile.full_name`
- Department from `profile.department`
- Year from `profile.year`
- CGPA from `academics.cgpa`

## System Architecture

### Application Framework
- **Flask Web Server**: Single-file architecture with `app.py` as the main entry point
- **Session Management**: Flask sessions with configurable timeout (default 30 minutes)
- **DEMO_MODE**: Critical toggle in `config.json` that controls whether actual forensic capture occurs or sample data is used

### Authentication & Authorization
- **Three-Tier User System**:
  1. **Students**: 6 legitimate users with full profile data stored in `model/data.json`
  2. **Real Admins**: 2 admin accounts (`admin` and `superadmin`) stored in `model/admin_settings.json`
  3. **Honeypot Credentials**: Fake admin credentials (e.g., `root/toor`) that trigger traps
- **Credential Validation**: Direct JSON file lookup without traditional hashing (educational context)
- **Session-Based Access Control**: Role-based routing to different dashboards

### Attack Detection System
- **Inline AI Classifier**: `SimpleAIClassifier` class embedded in `app.py` performs real-time pattern matching
- **Pattern Databases**: JSON files in `/ai_training/` directory containing attack signatures:
  - SQL injection patterns (109 signatures)
  - XSS patterns (183 signatures)
  - Brute force thresholds
  - Device spoofing indicators
  - IP hopping rules
  - Payload injection patterns
  - Reconnaissance paths
  - Behavioral anomalies
- **Risk Scoring**: 0-100 scale with severity classification (Low/Medium/High)
- **Multi-Vector Detection**: Single input can trigger multiple attack classifications

### Forensic Capture System (trap.py)
- **Unified Trap Function**: `trigger_trap()` coordinates all evidence collection
- **Three Evidence Types**:
  1. **Webcam Capture**: Uses OpenCV (cv2) in production, sample image in DEMO_MODE
  2. **Screenshot Recording**: PyAutoGUI captures every 5 seconds for 5 minutes (disabled in DEMO_MODE)
  3. **Keylogging**: pynput keyboard listener (uses sample data in DEMO_MODE)
- **Conditional Imports**: Optional dependencies only loaded when not in DEMO_MODE
- **Storage Locations**:
  - Images: `/Capture/intruder/`
  - Screenshots: `/Capture/screenshots/`
  - Logs: `/logs/` directory

### Data Storage Architecture
- **Hybrid Storage Model**: MongoDB primary with JSON fallback
- **MongoDB Collections** (when available):
  - `intrusions` - Main incident records
  - `captures` - Forensic evidence metadata
  - `keylogs` - Keystroke data
  - `locations` - Geolocation data
  - `ai_scores` - Classification results
  - `honeypot_events` - Trap activations
  - `login_attempts` - Authentication history
- **File-Based Fallback**: All data mirrored to `/logs/*.json` files when MongoDB unavailable
- **CSV Export**: `intruder_log.csv` for spreadsheet compatibility

### Frontend Architecture
- **Mobile-First Design**: 9:16 aspect ratio optimized for smartphone displays
- **Student Portal**:
  - Login page (`login.html`)
  - Dashboard (`student_dashboard.html`)
  - Profile viewer (`student_profile.html`)
  - Academic records (`student_academics.html`)
- **Admin Dashboards**:
  - Real admin (`admin_dashboard.html`) - Desktop web interface
  - Fake admin (`fake_admin.html`) - Mobile honeypot interface
- **Styling**: Malla Reddy University branding (Navy #0A2040, Orange #F57C00)
- **JavaScript**: `loading.js` provides loading animations across all pages

### Geolocation & Metadata
- **IP Resolution**: Flask request headers with X-Forwarded-For support
- **Public IP Fallback**: External API (ipify.org) when behind NAT
- **Geolocation API**: Configured in `config.json` with demo API key
- **Metadata Capture**:
  - User-Agent strings
  - MAC addresses (when available)
  - ISP information
  - GPS coordinates
  - City/State/Country

### Honeypot Mechanism
- **Credential-Based Trap**: Specific username/password combinations trigger immediate redirection
- **Fake Admin Dashboard**: Realistic-looking interface to keep attackers engaged
- **Background Evidence Collection**: Trap activates silently while attacker interacts with decoy
- **Trap Configuration**: `model/admin_settings.json` defines honeypot credentials

### Configuration Management
- **Central Config**: `config.json` contains all system settings
- **Key Configuration Options**:
  - `demo_mode`: Controls forensic capture behavior
  - `consent_required`: Legal compliance flag
  - MongoDB connection parameters
  - Screenshot intervals and durations
  - Session timeout values
  - API keys for external services

## External Dependencies

### Core Framework
- **Flask 3.0.0**: Web application framework
- **Flask-SocketIO 5.3.5**: Real-time communication (if needed for live updates)

### Database
- **pymongo 4.6.0**: MongoDB driver with fallback to JSON files
- **MongoDB**: Optional local instance on localhost:27017

### Forensic Capture (Optional)
- **opencv-python 4.8.1.78**: Webcam capture (only required in production mode)
- **PyAutoGUI 0.9.54**: Screenshot capture (only required in production mode)
- **pynput 1.7.6**: Keyboard logging (only required in production mode)
- **Pillow 10.1.0**: Image processing

### Data Processing
- **pandas 2.1.3**: CSV export and data analysis
- **fpdf 1.7.2**: PDF report generation

### Utilities
- **requests 2.31.0**: External API calls (IP geolocation)
- **psutil 5.9.6**: System information gathering

### Network
- **python-socketio 5.10.0**: WebSocket support

### Note on Dependencies
The application gracefully degrades when optional dependencies are unavailable. In DEMO_MODE, only Flask and basic Python libraries are strictly required, making it safe for presentation environments.