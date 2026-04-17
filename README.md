# WebLock  
### AI-Powered Cybersecurity & Digital Forensics System  

<p align="center">
  <img src="https://img.shields.io/badge/Security-AI%20Driven-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Detection-Real%20Time-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Framework-Flask-red?style=for-the-badge">
</p>

---

## Overview  

WebLock is an intelligent intrusion detection and digital forensics system designed to secure web applications against modern cyber threats.  
It combines real-time attack detection with automated evidence collection to provide both **prevention and post-incident analysis**.

---

## Problem  

Web applications are increasingly vulnerable to attacks such as SQL Injection, Cross-Site Scripting (XSS), and brute force attempts.  
Traditional security mechanisms often:
- Fail to detect sophisticated attack patterns  
- Lack behavioral analysis capabilities  
- Do not provide sufficient forensic evidence  

---

## Solution  

WebLock introduces a unified approach that integrates:
- Real-time threat detection  
- Behavioral analysis  
- Automated forensic data collection  
- Administrative monitoring  

This enables not only early detection but also detailed investigation of security incidents.

---

## Core Features  

### Attack Detection  
- SQL Injection  
- Cross-Site Scripting (XSS)  
- Brute Force Attacks  
- Session and Credential-based anomalies  

---

### Intrusion Monitoring  
- IP address tracking  
- Device and user-agent identification  
- Behavioral pattern analysis  
- Suspicious activity detection  

---

### Evidence Collection  
- Screen capture during suspicious activity  
- Webcam-based intruder capture (endpoint-level)  
- Keystroke logging  
- Structured activity logs  

---

### Forensic Reporting  
- Automated generation of forensic reports  
- Includes attack metadata, timestamps, and behavioral insights  
- Supports post-incident investigation  

---

### Administrative Interface  
- Centralized monitoring dashboard  
- Real-time visibility of system activity  
- Access to logs and forensic data  

---

## System Workflow  

1. User initiates a login request  
2. Input and behavior are analyzed  
3. Suspicious patterns are evaluated  
4. Threat is classified and logged  
5. Evidence is collected automatically  
6. Data is made available for analysis  

---

## Technology Stack  

| Layer        | Technology |
|-------------|------------|
| Backend     | Flask (Python) |
| AI Logic    | Pattern-based + Behavioral Analysis |
| Database    | MongoDB |
| Frontend    | HTML, CSS, JavaScript |
| Logging     | JSON / CSV |

---

## Installation  

```bash
git clone https://github.com/hitksh18/weblock.git
cd weblock
pip install -r requirements.txt
python app.py
