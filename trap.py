import os
import json
import csv
import time
import requests
import threading
import re
from datetime import datetime

# Optional imports (only when not in DEMO_MODE)
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    
try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

try:
    from flask import request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    request = None

# Configuration
BASE_DIR = os.getcwd()
LOGS_DIR = os.path.join(BASE_DIR, "logs")
CAPTURE_DIR = os.path.join(BASE_DIR, "Capture")
INTRUDER_DIR = os.path.join(CAPTURE_DIR, "intruder")
SCREENSHOT_DIR = os.path.join(CAPTURE_DIR, "screenshots")
INTRUDER_LOG_FILE = os.path.join(LOGS_DIR, "intruder_log.csv")
KEYLOG_JSON_FILE = os.path.join(LOGS_DIR, "key_logs.json")

# Load demo mode from config
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        DEMO_MODE = config.get("demo_mode", True)
except:
    DEMO_MODE = True

# Ensure Directories Exist
for directory in [LOGS_DIR, INTRUDER_DIR, SCREENSHOT_DIR]:
    os.makedirs(directory, exist_ok=True)

# Track captured intruders
captured_intruders = set()

def initialize_csv():
    """Creates CSV files with headers if they don't exist."""
    if not os.path.exists(INTRUDER_LOG_FILE):
        with open(INTRUDER_LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "IP", "City", "State", "Country", "Latitude", "Longitude", "ISP"])
        print(f"✅ Initialized {INTRUDER_LOG_FILE}")

def get_real_ip():
    """Retrieves the user's public IPv4 address."""
    try:
        if FLASK_AVAILABLE and request:
            if request.headers.get('X-Forwarded-For'):
                client_ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
            else:
                client_ip = request.remote_addr
        else:
            client_ip = "127.0.0.1"  

        private_ip_ranges = ["192.168.", "10.", "127.", "172."]
        if any(client_ip.startswith(prefix) for prefix in private_ip_ranges) or client_ip == "127.0.0.1":
            try:
                response = requests.get("https://api64.ipify.org?format=json", timeout=3)
                client_ip = response.json().get("ip", client_ip)
            except:
                pass

        return client_ip
    except Exception as e:
        print(f"⚠ Error getting IP: {e}")
        return "Unknown"

def get_geolocation(ip_address):
    """Fetches geolocation data based on IP address."""
    if DEMO_MODE:
        return {
            "city": "Hyderabad",
            "region": "Telangana",
            "country": "India",
            "latitude": "17.3850",
            "longitude": "78.4867",
            "isp": "ACT Fibernet"
        }
    
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=3)
        data = response.json()
        
        return {
            "city": data.get("city", "Unknown"),
            "region": data.get("regionName", "Unknown"),
            "country": data.get("country", "Unknown"),
            "latitude": str(data.get("lat", "Unknown")),
            "longitude": str(data.get("lon", "Unknown")),
            "isp": data.get("isp", "Unknown")
        }
    except Exception as e:
        print(f"⚠ Error fetching geolocation: {e}")
        return {
            "city": "Unknown",
            "region": "Unknown",
            "country": "Unknown",
            "latitude": "Unknown",
            "longitude": "Unknown",
            "isp": "Unknown"
        }

def log_intruder(ip_address, location_data):
    """Logs intruder details in the CSV file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row_data = [
        timestamp,
        ip_address,
        location_data.get("city", "Unknown"),
        location_data.get("region", "Unknown"),
        location_data.get("country", "Unknown"),
        location_data.get("latitude", "Unknown"),
        location_data.get("longitude", "Unknown"),
        location_data.get("isp", "Unknown")
    ]

    with open(INTRUDER_LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row_data)
    print(f"🔴 Intruder Logged: {ip_address} from {location_data.get('city', 'Unknown')}")

def sanitize_ip(ip_address):
    """Sanitize IP for filenames."""
    return re.sub(r'[^\w]', '_', ip_address)

def capture_intruder_image(ip_address):
    """Captures intruder image (DEMO MODE: uses sample image)."""
    if ip_address in captured_intruders:
        return None

    if DEMO_MODE:
        sample_image = os.path.join(INTRUDER_DIR, "sample_intruder.jpg")
        if not os.path.exists(sample_image) and CV2_AVAILABLE:
            import numpy as np
            demo_img = np.zeros((480, 640, 3), dtype=np.uint8)
            demo_img[:] = (40, 32, 10)  # Navy background
            cv2.putText(demo_img, "DEMO MODE", (180, 240), cv2.FONT_HERSHEY_BOLD, 1.5, (0, 124, 245), 3)
            cv2.imwrite(sample_image, demo_img)
        elif not os.path.exists(sample_image):
            print("⚠ OpenCV not available, skipping demo image creation")
            return None
        
        sanitized_ip = sanitize_ip(ip_address)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"intruder_{sanitized_ip}_{timestamp}.jpg"
        filepath = os.path.join(INTRUDER_DIR, filename)
        
        import shutil
        shutil.copy(sample_image, filepath)
        print(f"📸 [DEMO] Intruder Image: {filename}")
        captured_intruders.add(ip_address)
        return filename
    
    if not CV2_AVAILABLE:
        print("⚠ OpenCV not available")
        return None
        
    try:
        sanitized_ip = sanitize_ip(ip_address)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("⚠ Error: Could not open camera")
            return None

        ret, frame = cap.read()
        cap.release()

        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"intruder_{sanitized_ip}_{timestamp}.jpg"
            filepath = os.path.join(INTRUDER_DIR, filename)
            
            cv2.imwrite(filepath, frame)
            print(f"📸 Intruder Image Captured: {filepath}")
            captured_intruders.add(ip_address)
            return filename
    except Exception as e:
        print(f"⚠ Error capturing image: {e}")
    
    return None

def capture_screenshots(ip_address):
    """Captures screenshots (DEMO MODE: limited captures)."""
    sanitized_ip = sanitize_ip(ip_address)
    screenshot_count = 0
    max_screenshots = 3 if DEMO_MODE else 999999
    
    while screenshot_count < max_screenshots:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{sanitized_ip}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            
            if DEMO_MODE and CV2_AVAILABLE:
                import numpy as np
                demo_screenshot = np.zeros((900, 1440, 3), dtype=np.uint8)
                demo_screenshot[:] = (244, 243, 241)
                cv2.putText(demo_screenshot, f"DEMO Screenshot #{screenshot_count + 1}", 
                           (400, 450), cv2.FONT_HERSHEY_BOLD, 2, (64, 32, 10), 4)
                cv2.imwrite(filepath, demo_screenshot)
            elif DEMO_MODE:
                print(f"⚠ [DEMO] Screenshot #{screenshot_count + 1} (OpenCV not available)")
            elif PYAUTOGUI_AVAILABLE:
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
            else:
                print("⚠ pyautogui not available")
                break
            
            print(f"🖼 Screenshot Saved: {filename}")
            screenshot_count += 1
            time.sleep(5)
        except Exception as e:
            print(f"⚠ Screenshot error: {e}")
            break

class Keylogger:
    """Keylogger with JSON storage (DEMO MODE: simulated data)."""
    def __init__(self):
        self.log_file = KEYLOG_JSON_FILE
        self.logs = self.load_logs()
        self.demo_mode = DEMO_MODE

    def load_logs(self):
        """Loads existing logs from JSON."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                return json.load(f)
        return {}

    def save_logs(self):
        """Writes keylogs to JSON file."""
        with open(self.log_file, "w") as f:
            json.dump(self.logs, f, indent=4)

    def on_press(self, key):
        """Logs pressed keys in JSON format."""
        try:
            key_str = key.char.upper() if hasattr(key, 'char') else f"[{str(key).replace('Key.', '').upper()}]"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if timestamp not in self.logs:
                self.logs[timestamp] = []
            self.logs[timestamp].append(key_str)

            self.save_logs()
        except Exception as e:
            print(f"⚠ Keylogger error: {e}")

    def start(self):
        """Starts the keylogger."""
        if self.demo_mode:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logs[timestamp] = ["[DEMO]", "A", "D", "M", "I", "N", "[ENTER]", "P", "A", "S", "S", "[ENTER]"]
            self.save_logs()
            print(f"⌨ [DEMO] Keylogger simulated")
        elif PYNPUT_AVAILABLE:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            print(f"⌨ Keylogger started: {self.log_file}")
        else:
            print("⚠ pynput not available")

def trigger_trap(username=None, user_ip=None, user_mac=None, session_id=None, reason="detected_attack", metadata=None):
    """
    Main trap activation function - integrates with Flask app
    Triggers all forensic capture mechanisms and logs incident
    
    Args:
        username: Username from login attempt
        user_ip: User's IP address
        user_mac: User's MAC address
        session_id: Session identifier
        reason: Reason for trap activation
        metadata: Additional metadata (dict)
    
    Returns:
        dict: {incident_id, status, message}
    """
    if metadata is None:
        metadata = {}
    
    print(f"🚨 TRAP ACTIVATED: {reason}")
    print(f"   IP: {user_ip}, User: {username}")
    
    # Generate incident ID
    timestamp = datetime.now()
    incident_id = f"INC-{timestamp.strftime('%Y%m%d-%H%M%S')}"
    
    # Execute all traps
    execute_traps_internal(user_ip or "127.0.0.1")
    
    # Create intrusion record
    intrusion_data = {
        "incident_id": incident_id,
        "username": username,
        "user_ip": user_ip,
        "user_mac": user_mac,
        "session_id": session_id,
        "timestamp": timestamp,
        "reason": reason,
        "status": "captured",
        "attack_type": reason,
        "risk_score": metadata.get("risk_score", 75),
        "confidence": metadata.get("confidence", 85),
        "severity": "High" if metadata.get("risk_score", 75) > 70 else "Medium",
        "metadata": metadata
    }
    
    # Save to database
    try:
        import database
        location_data = get_geolocation(user_ip or "127.0.0.1")
        intrusion_data.update({
            "city": location_data.get("city"),
            "state": location_data.get("region"),
            "country": location_data.get("country"),
            "latitude": location_data.get("latitude"),
            "longitude": location_data.get("longitude"),
            "isp": location_data.get("isp")
        })
        database.save_intrusion(intrusion_data)
    except Exception as e:
        print(f"⚠ Database save error: {e}")
    
    print(f"✅ Trap executed successfully: {incident_id}")
    
    return {
        "incident_id": incident_id,
        "status": "success",
        "message": "Trap activated and evidence captured"
    }

def execute_traps_internal(ip_address):
    """Execute all traps (internal function)."""
    if ip_address in captured_intruders:
        print(f"⚠ Intruder {ip_address} already captured")
        return

    print(f"🚨 Executing traps for {ip_address}")
    
    # Initialize CSV
    initialize_csv()
    
    # Get location and log
    location_data = get_geolocation(ip_address)
    log_intruder(ip_address, location_data)
    
    # Capture intruder image
    capture_intruder_image(ip_address)
    
    # Start screenshot thread
    threading.Thread(target=capture_screenshots, args=(ip_address,), daemon=True).start()
    
    # Start keylogger
    Keylogger().start()
    
    print(f"✅ All traps executed for {ip_address}")
