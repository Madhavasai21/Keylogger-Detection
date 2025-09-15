# Keylogger Detection System Using Python
## Project overview
A cybersecurity tool designed to detect and prevent malicious keylogging activities using Python, process monitoring, behavioral analysis, and machine learning.
Keyloggers silently record keystrokes to steal sensitive data (passwords, banking details, confidential information). This project provides a real-time defense mechanism against such threats with alerts, logs, and a user-friendly interface.

---

# Features
- Real-Time Process Monitoring – Detects suspicious background processes.
- Machine Learning-Based Detection – Isolation Forest, Random Forest, and SVM models for anomaly detection.
- Behavioral Analysis – Identifies unusual keystroke patterns, hidden processes, and file I/O anomalies.
- Signature-Based Detection – Scans for known malicious processes and signatures.
- Real-Time Alerts & Logging – Generates pop-up alerts and logs suspicious activity.
- User-Friendly Interface – Built with Streamlit/Tkinter for easy visualization.
- Detection Accuracy (~93%) with confusion matrix and performance analysis.
- Cross-Platform – Runs on Windows, Linux, and macOS.

---
## Technologies Used
- **Programming Language:** Python 3.7+
- **Libraries & Frameworks:**
    - psutil, PyHook, PyInput (System monitoring)
    - scikit-learn, pandas, numpy (Machine Learning & Data Processing)
    - Streamlit / Tkinter (UI)
    - matplotlib, seaborn (Visualization)
- **Storage:** SQLite / CSV logs

---
# ⚙️ Installation & Setup
### 1.Clone the repository

```
git clone https://github.com/Madhavasai21/Keylogger-Detection.git
```
### 2.Install dependencies

```
pip install -r requirements.txt
```

### 3.Run the application

```
python train.py
python -m streamlit run app.py
```

# Usage
- Launch the application with streamlit run app.py.
- Start monitoring system processes.
- Suspicious activity triggers real-time alerts.
- View logs of detected keyloggers in the logs/ folder.
- Admins can terminate malicious processes from the dashboard.

---
#### 
## Interface
<img src="https://github.com/Madhavasai21/Keylogger-Detection/blob/main/images/Screenshot%202025-09-07%20114155.png" alt="Main interface"  width="400"/>

---
## Analysis Results
<img src="https://github.com/Madhavasai21/Keylogger-Detection/blob/main/images/Screenshot%202025-09-07%20114353.png"  width="400"/>

---
## Extacted Feautures
<img src="https://github.com/Madhavasai21/Keylogger-Detection/blob/main/images/Screenshot%202025-09-07%20114413.png"  width="400"/>

---

## Monitoring logs
<img src="https://github.com/Madhavasai21/Keylogger-Detection/blob/main/images/Screenshot%202025-09-07%20114442.png"  width="600" height="400"/>

---
## suspicious Strokes
<img src="https://github.com/Madhavasai21/Keylogger-Detection/blob/main/images/Screenshot%202025-09-07%20114739.png"  width="600"/>
