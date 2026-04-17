import json
import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load configuration
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {
        "mongodb": {"host": "localhost", "port": 27017, "database": "WebLock-db"},
        "demo_mode": True
    }

# MongoDB Connection
try:
    client = MongoClient(
        config["mongodb"]["host"],
        config["mongodb"]["port"],
        serverSelectionTimeoutMS=2000
    )
    client.admin.command('ping')
    db = client[config["mongodb"]["database"]]
    MONGODB_AVAILABLE = True
    print("✅ MongoDB connected successfully")
except (ConnectionFailure, Exception) as e:
    print(f"⚠️  MongoDB not available: {e}")
    print("📝 Running in file-only mode (data will be saved to JSON/CSV files)")
    MONGODB_AVAILABLE = False
    db = None

# Collections
if MONGODB_AVAILABLE:
    intrusions_col = db["intrusions"]
    captures_col = db["captures"]
    keylogs_col = db["keylogs"]
    locations_col = db["locations"]
    screenshots_col = db["screenshots"]
    intruder_images_col = db["intruder_images"]
    ai_scores_col = db["ai_scores"]
    reports_col = db["reports"]
    honeypot_events_col = db["honeypot_events"]
    suspicious_payloads_col = db["suspicious_payloads"]
    login_attempts_col = db["login_attempts"]
else:
    intrusions_col = None
    captures_col = None
    keylogs_col = None
    locations_col = None
    screenshots_col = None
    intruder_images_col = None
    ai_scores_col = None
    reports_col = None
    honeypot_events_col = None
    suspicious_payloads_col = None
    login_attempts_col = None

def save_intrusion(incident_data):
    """Save intrusion incident to MongoDB or JSON file"""
    if MONGODB_AVAILABLE:
        try:
            result = intrusions_col.insert_one(incident_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving intrusion: {e}")
    
    os.makedirs("logs", exist_ok=True)
    intrusions_file = "logs/intrusions.json"
    
    try:
        if os.path.exists(intrusions_file):
            with open(intrusions_file, "r") as f:
                intrusions = json.load(f)
        else:
            intrusions = []
        
        intrusion_copy = incident_data.copy()
        if "timestamp" in intrusion_copy and hasattr(intrusion_copy["timestamp"], "isoformat"):
            intrusion_copy["timestamp"] = intrusion_copy["timestamp"].isoformat()
        
        intrusions.append(intrusion_copy)
        
        with open(intrusions_file, "w") as f:
            json.dump(intrusions, f, indent=2, default=str)
        
        print(f"✅ Intrusion saved to file: {intrusions_file}")
        return incident_data.get("incident_id")
    except Exception as e:
        print(f"Error saving intrusion to file: {e}")
        return None

def save_ai_score(score_data):
    """Save AI classification score to MongoDB or JSON file"""
    if MONGODB_AVAILABLE:
        try:
            ai_scores_col.insert_one(score_data)
            return True
        except Exception as e:
            print(f"Error saving AI score: {e}")
    
    os.makedirs("logs", exist_ok=True)
    ai_scores_file = "logs/ai_scores.json"
    
    try:
        if os.path.exists(ai_scores_file):
            with open(ai_scores_file, "r") as f:
                scores = json.load(f)
        else:
            scores = []
        
        score_copy = score_data.copy()
        if "timestamp" in score_copy and hasattr(score_copy["timestamp"], "isoformat"):
            score_copy["timestamp"] = score_copy["timestamp"].isoformat()
        
        scores.append(score_copy)
        
        with open(ai_scores_file, "w") as f:
            json.dump(scores, f, indent=2, default=str)
        
        return True
    except Exception as e:
        print(f"Error saving AI score to file: {e}")
        return False

def save_location(location_data):
    """Save location data to MongoDB or JSON file"""
    if MONGODB_AVAILABLE:
        try:
            locations_col.insert_one(location_data)
            return True
        except Exception as e:
            print(f"Error saving location: {e}")
    
    os.makedirs("logs", exist_ok=True)
    locations_file = "logs/locations.json"
    
    try:
        if os.path.exists(locations_file):
            with open(locations_file, "r") as f:
                locations = json.load(f)
        else:
            locations = []
        
        locations.append(location_data)
        
        with open(locations_file, "w") as f:
            json.dump(locations, f, indent=2, default=str)
        
        return True
    except Exception as e:
        print(f"Error saving location to file: {e}")
        return False

def save_capture(capture_data):
    """Save capture metadata to MongoDB or JSON file"""
    if MONGODB_AVAILABLE:
        try:
            captures_col.insert_one(capture_data)
            return True
        except Exception as e:
            print(f"Error saving capture: {e}")
    
    os.makedirs("logs", exist_ok=True)
    captures_file = "logs/captures.json"
    
    try:
        if os.path.exists(captures_file):
            with open(captures_file, "r") as f:
                captures = json.load(f)
        else:
            captures = []
        
        capture_copy = capture_data.copy()
        if "timestamp" in capture_copy and hasattr(capture_copy["timestamp"], "isoformat"):
            capture_copy["timestamp"] = capture_copy["timestamp"].isoformat()
        
        captures.append(capture_copy)
        
        with open(captures_file, "w") as f:
            json.dump(captures, f, indent=2, default=str)
        
        return True
    except Exception as e:
        print(f"Error saving capture to file: {e}")
        return False

def save_login_attempt(attempt_data):
    """Save login attempt to MongoDB or JSON file"""
    if MONGODB_AVAILABLE:
        try:
            login_attempts_col.insert_one(attempt_data)
            return True
        except Exception as e:
            print(f"Error saving login attempt: {e}")
    
    os.makedirs("logs", exist_ok=True)
    login_attempts_file = "logs/login_attempts.json"
    
    try:
        if os.path.exists(login_attempts_file):
            with open(login_attempts_file, "r") as f:
                attempts = json.load(f)
        else:
            attempts = []
        
        attempt_copy = attempt_data.copy()
        if "timestamp" in attempt_copy and hasattr(attempt_copy["timestamp"], "isoformat"):
            attempt_copy["timestamp"] = attempt_copy["timestamp"].isoformat()
        
        attempts.append(attempt_copy)
        
        with open(login_attempts_file, "w") as f:
            json.dump(attempts, f, indent=2, default=str)
        
        return True
    except Exception as e:
        print(f"Error saving login attempt to file: {e}")
        return False

def get_all_intrusions():
    """Retrieve all intrusions from MongoDB or JSON file"""
    if MONGODB_AVAILABLE:
        try:
            return list(intrusions_col.find().sort("timestamp", -1))
        except Exception as e:
            print(f"Error retrieving intrusions: {e}")
    
    intrusions_file = "logs/intrusions.json"
    try:
        if os.path.exists(intrusions_file):
            with open(intrusions_file, "r") as f:
                intrusions = json.load(f)
            intrusions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return intrusions
    except Exception as e:
        print(f"Error reading intrusions from file: {e}")
    
    return []

def get_intrusion_by_id(incident_id):
    """Retrieve specific intrusion by incident_id"""
    if MONGODB_AVAILABLE:
        try:
            return intrusions_col.find_one({"incident_id": incident_id})
        except Exception as e:
            print(f"Error retrieving intrusion: {e}")
    return None

def get_intrusion_stats():
    """Get statistics for admin dashboard"""
    stats = {
        "total_intrusions": 0,
        "attack_types": {},
        "countries": {},
        "timeline": []
    }
    
    intrusions = get_all_intrusions()
    stats["total_intrusions"] = len(intrusions)
    
    for intrusion in intrusions:
        attack_type = intrusion.get("attack_type", "Unknown")
        stats["attack_types"][attack_type] = stats["attack_types"].get(attack_type, 0) + 1
        
        country = intrusion.get("country", "Unknown")
        stats["countries"][country] = stats["countries"].get(country, 0) + 1
    
    return stats

def upload_all_data():
    """Upload existing CSV/JSON data to MongoDB"""
    if not MONGODB_AVAILABLE:
        print("MongoDB not available, skipping upload")
        return
    
    print("📤 Uploading existing data to MongoDB...")
    
    # Upload intruder log CSV
    try:
        import csv
        if os.path.exists("logs/intruder_log.csv"):
            with open("logs/intruder_log.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("IP"):
                        save_location(row)
    except Exception as e:
        print(f"Error uploading CSV data: {e}")
    
    print("✅ Data upload complete")
