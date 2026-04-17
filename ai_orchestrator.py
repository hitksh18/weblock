"""
AI Orchestrator - Real-time Pattern Learning and Threat Intelligence Integration
Automatically learns from new attacks and integrates external threat feeds
"""

import json
import os
import requests
from datetime import datetime
from collections import Counter

class AIOrchestrator:
    def __init__(self):
        self.pattern_dir = 'ai_training'
        self.archive_dir = 'ai_training/archive'
        self.logs_dir = 'logs'
        
        # Create directories if they don't exist
        os.makedirs(self.archive_dir, exist_ok=True)
        
    def learn_from_attack(self, attack_data):
        """
        Learn new patterns from detected attacks
        """
        # Normalize attack type to match existing pattern filenames
        attack_type_raw = attack_data.get('attack_type', '')
        
        # Map common attack types to canonical filenames
        type_mapping = {
            'sql injection': 'sql_injection',
            'cross-site scripting (xss)': 'xss',
            'xss': 'xss',
            'brute force': 'brute_force',
            'honeypot credentials used': 'honeypot',
            'device spoofing': 'device_spoofing',
            'ip hopping': 'ip_hopping'
        }
        
        attack_type = type_mapping.get(attack_type_raw.lower(), attack_type_raw.lower().replace(' ', '_'))
        pattern_file = f'{self.pattern_dir}/{attack_type}.json'
        
        # Extract pattern from attack - prioritize password field (where malicious payloads usually are)
        username = attack_data.get('username', '')
        password = attack_data.get('password', '')
        payload = attack_data.get('payload', '')
        user_input = attack_data.get('user_input', '')
        
        # Determine which field contains the malicious pattern
        # For SQLi/XSS attacks, the payload is usually in password or username field
        # Choose the field that triggered the detection
        malicious_pattern = password or username or payload or user_input
        
        # Skip if pattern is empty or too generic
        if not malicious_pattern or len(malicious_pattern) < 2:
            return False
        
        new_pattern = {
            'pattern': malicious_pattern,
            'description': f'Learned from {attack_data.get("incident_id", "unknown")}',
            'severity': attack_data.get('severity', 'Medium'),
            'confidence': attack_data.get('confidence', 80),
            'timestamp': datetime.now().isoformat(),
            'source': 'real_attack',
            'risk_score': attack_data.get('risk_score', 50)
        }
        
        # Load existing patterns
        if os.path.exists(pattern_file):
            with open(pattern_file, 'r') as f:
                patterns = json.load(f)
        else:
            patterns = {'patterns': []}
        
        # Check if pattern already exists (handle both string and dict formats)
        existing_patterns = patterns.get('patterns', [])
        pattern_already_exists = False
        
        for p in existing_patterns:
            if isinstance(p, str):
                # Old format: patterns are strings
                if p == malicious_pattern:
                    pattern_already_exists = True
                    break
            elif isinstance(p, dict):
                # New format: patterns are dicts
                if p.get('pattern') == malicious_pattern:
                    pattern_already_exists = True
                    break
        
        if not pattern_already_exists:
            patterns['patterns'].append(new_pattern)
            
            # Save updated patterns
            with open(pattern_file, 'w') as f:
                json.dump(patterns, f, indent=2)
            
            print(f"✅ Learned new {attack_type} pattern: {malicious_pattern[:50]}")
            return True
        return False
    
    def check_ip_reputation(self, ip_address):
        """
        Check IP reputation using AbuseIPDB API (free tier)
        Returns threat score and category
        """
        # For demo/educational purposes, we'll simulate IP reputation
        # In production, you would use: api_key = os.getenv('ABUSEIPDB_API_KEY')
        
        # Simulate IP reputation check
        known_bad_ips = {
            '192.168.1.100': {'threat_score': 95, 'category': 'Brute Force'},
            '10.0.0.50': {'threat_score': 85, 'category': 'SQL Injection'},
        }
        
        if ip_address in known_bad_ips:
            return known_bad_ips[ip_address]
        
        # Check if IP is from known malicious ranges
        if ip_address.startswith('192.168') or ip_address.startswith('10.'):
            return {'threat_score': 10, 'category': 'Internal Network'}
        
        return {'threat_score': 0, 'category': 'Unknown'}
    
    def integrate_threat_intelligence(self, source='manual'):
        """
        Integrate threat intelligence from external sources
        """
        # Simulated threat intelligence data
        # In production, this would fetch from APIs like:
        # - AbuseIPDB
        # - VirusTotal
        # - AlienVault OTX
        # - CISA Known Exploited Vulnerabilities
        
        threat_intel = {
            'new_patterns': [
                {
                    'pattern': "admin' AND '1'='1",
                    'type': 'sql_injection',
                    'severity': 'Critical',
                    'confidence': 95,
                    'source': 'external_feed'
                },
                {
                    'pattern': '<script>eval(atob(',
                    'type': 'xss',
                    'severity': 'High',
                    'confidence': 90,
                    'source': 'external_feed'
                }
            ]
        }
        
        learned_count = 0
        for pattern_data in threat_intel['new_patterns']:
            pattern_type = pattern_data['type']
            pattern_file = f'{self.pattern_dir}/{pattern_type}.json'
            
            if os.path.exists(pattern_file):
                with open(pattern_file, 'r') as f:
                    patterns = json.load(f)
                
                # Check if pattern exists (handle both string and dict formats)
                pattern_already_exists = False
                new_pattern_str = pattern_data['pattern']
                
                for p in patterns.get('patterns', []):
                    if isinstance(p, str):
                        if p == new_pattern_str:
                            pattern_already_exists = True
                            break
                    elif isinstance(p, dict):
                        if p.get('pattern') == new_pattern_str:
                            pattern_already_exists = True
                            break
                
                if not pattern_already_exists:
                    patterns['patterns'].append(pattern_data)
                    with open(pattern_file, 'w') as f:
                        json.dump(patterns, f, indent=2)
                    learned_count += 1
        
        return {
            'status': 'success',
            'patterns_added': learned_count,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_pattern_stats(self):
        """
        Get statistics about learned patterns (handles both string and dict formats)
        """
        stats = {}
        total = 0
        
        for filename in os.listdir(self.pattern_dir):
            if filename.endswith('.json') and filename != 'archive':
                filepath = os.path.join(self.pattern_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        patterns = data.get('patterns', [])
                        # Count patterns (works for both string and dict entries)
                        count = len(patterns) if isinstance(patterns, list) else 0
                        stats[filename.replace('.json', '')] = count
                        total += count
                except Exception as e:
                    print(f"⚠️  Error reading {filename}: {e}")
                    pass
        
        stats['total'] = total
        return stats
    
    def archive_patterns(self):
        """
        Archive current patterns with timestamp
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_path = os.path.join(self.archive_dir, timestamp)
        os.makedirs(archive_path, exist_ok=True)
        
        for filename in os.listdir(self.pattern_dir):
            if filename.endswith('.json'):
                src = os.path.join(self.pattern_dir, filename)
                dst = os.path.join(archive_path, filename)
                with open(src, 'r') as f:
                    data = json.load(f)
                with open(dst, 'w') as f:
                    json.dump(data, f, indent=2)
        
        return f'Patterns archived to {archive_path}'

# Global instance
orchestrator = AIOrchestrator()
