from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime
from trap import trigger_trap
import database
from ai_orchestrator import orchestrator

# Simple AI classifier inline
class SimpleAIClassifier:
    def classify_attack(self, username="", password="", user_input="", ip="", mac="", metadata=None):
        if metadata is None:
            metadata = {}
        
        detected_attacks = []
        risk_score = 0
        
        # Check SQL Injection
        sql_patterns = ["'", "--", "OR", "UNION", "SELECT", "DROP", "INSERT", ";"]
        if any(p.lower() in username.lower() or p.lower() in password.lower() for p in sql_patterns):
            detected_attacks.append("SQL Injection")
            risk_score = max(risk_score, 90)
        
        # Check XSS
        xss_patterns = ["<script", "javascript:", "onerror=", "onload="]
        if any(p.lower() in username.lower() or p.lower() in password.lower() for p in xss_patterns):
            detected_attacks.append("Cross-Site Scripting (XSS)")
            risk_score = max(risk_score, 85)
        
        # Check brute force
        if metadata.get("failed_attempts", 0) >= 3:
            detected_attacks.append("Brute Force")
            risk_score = max(risk_score, 75)
        
        return {
            "attack_type": detected_attacks[0] if detected_attacks else "Unknown",
            "confidence": 90 if detected_attacks else 0,
            "risk_score": risk_score,
            "severity": "High" if risk_score > 70 else ("Medium" if risk_score > 40 else "Low"),
            "all_attacks_detected": detected_attacks,
            "features_used": ["Pattern matching", "Behavior analysis"]
        }

ai_classifier = SimpleAIClassifier()

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'weblock-demo-secret-key-2024')

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

DEMO_MODE = config.get("demo_mode", True)

# Track login attempts and user behavior
login_attempts = {}
user_sessions = {}
user_locations = {}
suspicious_paths_accessed = set()

# Load user data
def load_json(file_name):
    try:
        with open(f"model/{file_name}", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_users():
    return load_json("data.json").get("users", [])

def load_admin_users():
    return load_json("admin_settings.json").get("admin_users", [])

@app.route('/')
def index():
    """Login page"""
    return render_template('login.html', demo_mode=DEMO_MODE)

@app.route('/login', methods=['POST'])
def login():
    """Process login and detect attacks"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Get user IP (for demo, use localhost)
    user_ip = request.remote_addr or "127.0.0.1"
    user_mac = "00:00:00:00:00:00"  # In real scenario, would capture MAC
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    print(f"🔍 Login attempt: {username} from {user_ip}")
    
    # Track failed login attempts per IP
    if user_ip not in login_attempts:
        login_attempts[user_ip] = {
            "count": 0,
            "last_attempt": None,
            "usernames_tried": set(),
            "user_agents": set()
        }
    
    login_attempts[user_ip]["count"] += 1
    login_attempts[user_ip]["last_attempt"] = datetime.now()
    login_attempts[user_ip]["usernames_tried"].add(username)
    login_attempts[user_ip]["user_agents"].add(user_agent)
    
    # Detect device spoofing (user agent changes for same IP)
    device_mismatch = len(login_attempts[user_ip]["user_agents"]) > 1
    
    # Detect brute force (multiple usernames from same IP)
    failed_attempts = login_attempts[user_ip]["count"]
    
    # Detect suspicious behavior
    behavioral_anomaly = (
        failed_attempts > 2 or 
        len(login_attempts[user_ip]["usernames_tried"]) > 3 or
        len(password) > 100
    )
    
    # Log login attempt
    database.save_login_attempt({
        "username": username,
        "ip": user_ip,
        "mac": user_mac,
        "timestamp": datetime.now(),
        "user_agent": user_agent,
        "failed_attempts": failed_attempts
    })
    
    # Prepare metadata for AI classifier
    metadata = {
        "user_agent": user_agent,
        "failed_attempts": failed_attempts,
        "device_mismatch": device_mismatch,
        "geo_anomaly": False,
        "suspicious_path": False,
        "behavioral_anomaly": behavioral_anomaly
    }
    
    # Check for suspicious patterns using AI
    ai_result = ai_classifier.classify_attack(
        username=username,
        password=password,
        user_input="",
        ip=user_ip,
        mac=user_mac,
        metadata=metadata
    )
    
    # Check credentials for legitimate users
    users = load_users()
    admin_users = load_admin_users()
    admin_settings = load_json("admin_settings.json")
    fake_admin_creds = admin_settings.get("fake_admin_credentials", [])
    
    # Check for fake admin credentials (honeypot) - TRIGGER TRAP
    for fake_cred in fake_admin_creds:
        if fake_cred["username"] == username and fake_cred.get("password") == password:
            print(f"🎭 HONEYPOT TRIGGERED: Fake admin login attempt with {username}")
            
            metadata_extended = metadata.copy()
            metadata_extended.update({
                "risk_score": 95,
                "confidence": 100,
                "all_attacks_detected": ["Honeypot Credentials Used"],
                "honeypot_username": username
            })
            
            trap_result = trigger_trap(
                username=username,
                user_ip=user_ip,
                user_mac=user_mac,
                session_id=request.cookies.get('session'),
                reason="Honeypot Credentials - Fake Admin Login",
                metadata=metadata_extended
            )
            
            # Redirect to fake admin (honeypot)
            session['intruder'] = True
            session['incident_id'] = trap_result['incident_id']
            return redirect(url_for('fake_admin'))
    
    # If attack detected via AI, trigger trap
    if ai_result["risk_score"] > 0:
        print(f"🚨 ATTACK DETECTED: {ai_result['attack_type']} (Risk: {ai_result['risk_score']})")
        
        # Learn from this attack automatically (AI Pattern Learning)
        # Include both username and password so AI can extract the malicious payload
        attack_data = {
            'incident_id': 'temp_id',  # Will be set after trap trigger
            'username': username,
            'password': password,
            'attack_type': ai_result['attack_type'],
            'confidence': ai_result['confidence'],
            'risk_score': ai_result['risk_score'],
            'severity': ai_result['severity'],
            'all_attacks': ai_result.get('all_attacks_detected', [])
        }
        learned = orchestrator.learn_from_attack(attack_data)
        if learned:
            print(f"🤖 AI learned new pattern from {ai_result['attack_type']}")
        
        metadata_extended = metadata.copy()
        metadata_extended.update({
            "risk_score": ai_result["risk_score"],
            "confidence": ai_result["confidence"],
            "all_attacks_detected": ai_result["all_attacks_detected"]
        })
        
        trap_result = trigger_trap(
            username=username,
            user_ip=user_ip,
            user_mac=user_mac,
            session_id=request.cookies.get('session'),
            reason=ai_result['attack_type'],
            metadata=metadata_extended
        )
        
        # Redirect to fake admin (honeypot)
        session['intruder'] = True
        session['incident_id'] = trap_result['incident_id']
        return redirect(url_for('fake_admin'))
    
    # Check real admin credentials
    for user in admin_users:
        if user["username"] == username and user.get("password") == password:
            session['admin'] = username
            session['admin_role'] = user.get('role', 'admin')
            print(f"✅ Real admin login: {username}")
            return redirect(url_for('admin_dashboard'))
    
    # Check regular user
    for user in users:
        if user["username"] == username and user.get("password") == password:
            session['user'] = username
            # Reset failed attempts on successful login
            if user_ip in login_attempts:
                login_attempts[user_ip]["count"] = 0
            return redirect(url_for('student_dashboard'))
    
    # Invalid credentials - continue tracking
    return render_template('login.html', error="Invalid credentials", demo_mode=DEMO_MODE)

@app.route('/student')
def student_dashboard():
    """Student dashboard for legitimate users"""
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('student_dashboard.html', username=session.get('user'))

@app.route('/student/profile')
def student_profile():
    """Student profile page"""
    if 'user' not in session:
        return redirect(url_for('index'))
    
    users = load_users()
    user_data = None
    for user in users:
        if user.get("username") == session.get('user'):
            user_data = user
            break
    
    return render_template('student_profile.html', user=user_data, username=session.get('user'))

@app.route('/student/academics')
def student_academics():
    """Student academics page"""
    if 'user' not in session:
        return redirect(url_for('index'))
    
    users = load_users()
    user_data = None
    for user in users:
        if user.get("username") == session.get('user'):
            user_data = user
            break
    
    return render_template('student_academics.html', user=user_data, username=session.get('user'))

@app.route('/fake_admin', methods=['GET', 'POST'])
def fake_admin():
    """Fake admin page (honeypot)"""
    return render_template('fake_admin.html')

@app.route('/admin')
def admin_dashboard():
    """Real admin dashboard - comprehensive forensic panel"""
    if 'dash_user' not in session and 'admin' not in session:
        return redirect(url_for('index'))
    
    # Get intrusion data
    intrusions = database.get_all_intrusions()
    stats = database.get_intrusion_stats()
    
    # Get student data
    students = load_users()
    
    # Get honeypot events (intrusions that used fake credentials)
    honeypot_events = [i for i in intrusions if 'honeypot' in i.get('reason', '').lower() or 
                       'fake' in i.get('reason', '').lower()]
    
    # Calculate AI pattern counts
    ai_patterns = {
        'sql_count': 109,  # From ai_training/sql_injection.json
        'xss_count': 183,  # From ai_training/xss.json
        'brute_count': 15,  # From ai_training/bruteforce.json
        'total': 400  # Total patterns across all files
    }
    
    return render_template('admin.html', 
                          intrusions=intrusions,
                          stats=stats,
                          students=students,
                          honeypot_events=honeypot_events,
                          ai_patterns=ai_patterns,
                          demo_mode=DEMO_MODE)

@app.route('/api/incidents')
def api_incidents():
    """API endpoint to get all incidents"""
    intrusions = database.get_all_intrusions()
    # Convert ObjectId to string for JSON serialization
    for intrusion in intrusions:
        if '_id' in intrusion:
            intrusion['_id'] = str(intrusion['_id'])
        if 'timestamp' in intrusion:
            intrusion['timestamp'] = str(intrusion['timestamp'])
    return jsonify(intrusions)

@app.route('/api/stats')
def api_stats():
    """API endpoint to get statistics"""
    stats = database.get_intrusion_stats()
    return jsonify(stats)

@app.route('/api/analytics/realtime')
def api_analytics_realtime():
    """Real-time analytics data for charts"""
    intrusions = database.get_all_intrusions()
    
    # Attack type distribution
    attack_types = {}
    for i in intrusions:
        attack_type = i.get('attack_type', 'Unknown')
        attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
    
    # Timeline data (last 7 days)
    from collections import defaultdict
    from datetime import datetime, timedelta
    timeline = defaultdict(int)
    now = datetime.now()
    for i in range(7):
        date = (now - timedelta(days=i)).strftime('%Y-%m-%d')
        timeline[date] = 0
    
    for i in intrusions:
        if 'timestamp' in i:
            try:
                ts = i['timestamp']
                if isinstance(ts, str):
                    date = ts.split('T')[0]
                    if date in timeline:
                        timeline[date] += 1
            except:
                pass
    
    # Country distribution
    countries = {}
    for i in intrusions:
        country = i.get('country', 'Unknown')
        countries[country] = countries.get(country, 0) + 1
    
    # Risk score distribution
    risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
    for i in intrusions:
        risk = i.get('risk_score', 0)
        if risk > 70:
            risk_distribution['high'] += 1
        elif risk > 40:
            risk_distribution['medium'] += 1
        else:
            risk_distribution['low'] += 1
    
    # IP reputation data
    unique_ips = set()
    for i in intrusions:
        unique_ips.add(i.get('user_ip', ''))
    
    return jsonify({
        'attack_types': attack_types,
        'timeline': dict(sorted(timeline.items())),
        'countries': countries,
        'risk_distribution': risk_distribution,
        'total_intrusions': len(intrusions),
        'unique_ips': len(unique_ips),
        'high_risk_count': risk_distribution['high']
    })

@app.route('/api/ai/performance')
def api_ai_performance():
    """AI model performance metrics"""
    intrusions = database.get_all_intrusions()
    
    total_detections = len(intrusions)
    high_confidence = sum(1 for i in intrusions if i.get('confidence', 0) >= 80)
    
    # Calculate accuracy by attack type
    accuracy_by_type = {}
    for i in intrusions:
        attack_type = i.get('attack_type', 'Unknown')
        confidence = i.get('confidence', 0)
        if attack_type not in accuracy_by_type:
            accuracy_by_type[attack_type] = []
        accuracy_by_type[attack_type].append(confidence)
    
    avg_accuracy = {}
    for attack_type, confidences in accuracy_by_type.items():
        avg_accuracy[attack_type] = sum(confidences) / len(confidences) if confidences else 0
    
    # Get real pattern counts from AI orchestrator
    ai_patterns = orchestrator.get_pattern_stats()
    
    return jsonify({
        'total_detections': total_detections,
        'high_confidence_rate': (high_confidence / total_detections * 100) if total_detections > 0 else 0,
        'accuracy_by_type': avg_accuracy,
        'pattern_counts': ai_patterns,
        'avg_confidence': sum(i.get('confidence', 0) for i in intrusions) / total_detections if total_detections > 0 else 0
    })

@app.route('/api/ai/train', methods=['POST'])
def api_ai_train():
    """Manually trigger AI training from new patterns"""
    if 'dash_user' not in session and 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    result = orchestrator.integrate_threat_intelligence(source='manual')
    return jsonify(result)

@app.route('/api/threat-intel/ip/<ip_address>')
def api_threat_intel_ip(ip_address):
    """Check IP reputation using threat intelligence"""
    if 'dash_user' not in session and 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    reputation = orchestrator.check_ip_reputation(ip_address)
    return jsonify(reputation)

@app.route('/api/ai/patterns')
def api_ai_patterns():
    """Get current AI pattern statistics"""
    stats = orchestrator.get_pattern_stats()
    return jsonify(stats)

@app.route('/api/captured-files')
def api_captured_files():
    """Get list of captured images and screenshots"""
    if 'dash_user' not in session and 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    files = []
    
    # Check Capture/intruder directory
    intruder_dir = 'Capture/intruder'
    if os.path.exists(intruder_dir):
        for filename in os.listdir(intruder_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(intruder_dir, filename)
                size = os.path.getsize(filepath)
                files.append({
                    'name': filename,
                    'path': filepath.replace('\\', '/'),
                    'size': f'{size / 1024:.2f} KB'
                })
    
    # Check Capture/screenshots directory
    screenshots_dir = 'Capture/screenshots'
    if os.path.exists(screenshots_dir):
        for filename in os.listdir(screenshots_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(screenshots_dir, filename)
                size = os.path.getsize(filepath)
                files.append({
                    'name': filename,
                    'path': filepath.replace('\\', '/'),
                    'size': f'{size / 1024:.2f} KB'
                })
    
    return jsonify({'files': files})

@app.route('/api/keylog-files')
def api_keylog_files():
    """Get list of keylog files"""
    if 'dash_user' not in session and 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    files = []
    logs_dir = 'logs'
    
    if os.path.exists(logs_dir):
        for filename in os.listdir(logs_dir):
            if 'key' in filename.lower() and filename.endswith('.json'):
                filepath = os.path.join(logs_dir, filename)
                size = os.path.getsize(filepath)
                files.append({
                    'name': filename,
                    'path': filepath.replace('\\', '/'),
                    'size': f'{size / 1024:.2f} KB'
                })
    
    return jsonify({'files': files})

@app.route('/api/keylog-content')
def api_keylog_content():
    """Get content of a keylog file"""
    if 'dash_user' not in session and 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    filepath = request.args.get('file', '')
    
    # Security: prevent directory traversal
    if '..' in filepath or filepath.startswith('/'):
        return jsonify({'error': 'Invalid file path'}), 400
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/evidence/<incident_id>')
def evidence_viewer(incident_id):
    """Forensic evidence viewer page"""
    if 'dash_user' not in session and 'admin' not in session:
        return redirect(url_for('index'))
    
    # Get incident data
    intrusions = database.get_all_intrusions()
    incident = None
    for i in intrusions:
        if i.get('incident_id') == incident_id:
            incident = i
            break
    
    if not incident:
        return "Incident not found", 404
    
    # Get screenshots for this incident
    screenshots = []
    if 'screenshots' in incident:
        screenshots = incident['screenshots']
    
    # Get keylogs for this incident  
    keylogs = []
    if 'keylogs' in incident:
        keylogs = incident['keylogs']
    
    return render_template('evidence_viewer.html',
                          incident=incident,
                          screenshots=screenshots,
                          keylogs=keylogs)

@app.route('/generate-report/<incident_id>')
def generate_report(incident_id):
    """Generate PDF forensic report"""
    if 'dash_user' not in session and 'admin' not in session:
        return redirect(url_for('index'))
    
    from flask import send_file
    from fpdf import FPDF
    
    # Get incident data
    intrusions = database.get_all_intrusions()
    incident = None
    for i in intrusions:
        if i.get('incident_id') == incident_id:
            incident = i
            break
    
    if not incident:
        return "Incident not found", 404
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # Title
    pdf.cell(0, 10, 'FORENSIC INCIDENT REPORT', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Incident ID: {incident_id}', 0, 1, 'C')
    pdf.ln(5)
    
    # Incident Overview
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '1. INCIDENT OVERVIEW', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"Timestamp: {incident.get('timestamp', 'N/A')}", 0, 1)
    pdf.cell(0, 7, f"Attack Type: {incident.get('reason', 'Unknown')}", 0, 1)
    pdf.cell(0, 7, f"Risk Score: {incident.get('risk_score', 0)}/100", 0, 1)
    pdf.cell(0, 7, f"Severity: {'High' if incident.get('risk_score', 0) > 70 else ('Medium' if incident.get('risk_score', 0) > 40 else 'Low')}", 0, 1)
    pdf.ln(5)
    
    # Network Information
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. NETWORK INFORMATION', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"IP Address: {incident.get('ip', 'Unknown')}", 0, 1)
    pdf.cell(0, 7, f"MAC Address: {incident.get('mac', 'N/A')}", 0, 1)
    pdf.cell(0, 7, f"ISP: {incident.get('isp', 'Unknown')}", 0, 1)
    pdf.ln(5)
    
    # Geolocation
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. GEOLOCATION', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"City: {incident.get('city', 'Unknown')}", 0, 1)
    pdf.cell(0, 7, f"State: {incident.get('state', 'Unknown')}", 0, 1)
    pdf.cell(0, 7, f"Country: {incident.get('country', 'Unknown')}", 0, 1)
    pdf.cell(0, 7, f"Coordinates: {incident.get('latitude', 'N/A')}, {incident.get('longitude', 'N/A')}", 0, 1)
    pdf.ln(5)
    
    # Attack Details
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '4. ATTACK DETAILS', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"Username Attempted: {incident.get('username', 'N/A')}", 0, 1)
    metadata = incident.get('metadata', {})
    attacks = metadata.get('all_attacks_detected', [])
    if attacks:
        pdf.cell(0, 7, f"Detected Patterns: {', '.join(attacks)}", 0, 1)
    pdf.cell(0, 7, f"Confidence: {metadata.get('confidence', 'N/A')}%", 0, 1)
    pdf.ln(5)
    
    # Device Fingerprint
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '5. DEVICE FINGERPRINT', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"User Agent: {incident.get('user_agent', 'N/A')[:80]}", 0, 1)
    pdf.cell(0, 7, f"Session ID: {incident.get('session_id', 'N/A')}", 0, 1)
    pdf.ln(5)
    
    # Evidence Collected
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '6. EVIDENCE COLLECTED', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, f"Webcam Image: {'Yes' if incident.get('image_path') else 'No'}", 0, 1)
    pdf.cell(0, 7, f"Screenshots: {len(incident.get('screenshots', []))} captured", 0, 1)
    pdf.cell(0, 7, f"Keystrokes: {len(incident.get('keylogs', []))} logged", 0, 1)
    pdf.ln(10)
    
    # Footer
    pdf.set_font('Arial', 'I', 9)
    pdf.cell(0, 10, 'Generated by WebLock Intrusion Detection System', 0, 1, 'C')
    pdf.cell(0, 5, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
    
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Save PDF
    pdf_path = f'reports/{incident_id}.pdf'
    pdf.output(pdf_path)
    
    # Send file
    return send_file(pdf_path,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f'forensic_report_{incident_id}.pdf')

@app.route('/export/csv')
def export_csv():
    """Export intrusion data to CSV"""
    if 'dash_user' not in session and 'admin' not in session:
        return redirect(url_for('index'))
    
    # CSV file already exists at logs/intruder_log.csv
    from flask import send_file
    try:
        return send_file('logs/intruder_log.csv',
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name='intrusion_report.csv')
    except:
        return jsonify({'error': 'CSV file not found'}), 404

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/Capture/<path:filename>')
def serve_capture(filename):
    """Serve captured files (images, screenshots)"""
    from flask import send_from_directory
    return send_from_directory('Capture', filename)

@app.route('/demo')
def demo_info():
    """Demo information page"""
    return render_template('demo_info.html', config=config)

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 WebLock - Intrusion Detection System")
    print("=" * 60)
    print(f"📝 DEMO MODE: {DEMO_MODE}")
    print(f"🌐 Access the application at: http://72.61.231.238")
    print()
    print("🧪 Test SQL Injection Detection:")
    print("   Email: admin'--@test.com")
    print("   Password: admin' OR 'x'='x")
    print()
    print("✅ Valid Credentials:")
    print("   Admin Dashboard: admin1825 / admin@1825")
    print("   Student Portal: 2211cs040100@mru.edu.in / Student@100")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
