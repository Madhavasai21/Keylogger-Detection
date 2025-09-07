import streamlit as st
import numpy as np
import joblib
import os
import psutil
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import re
from datetime import datetime

# Load model
model = joblib.load("keylogger_model.pkl")

# Constants
LOG_FILE = "keylogger_alerts.log"
known_keyloggers = [
    # Common keyloggers
    "keylogger.exe", "keylog.exe", "kl.exe", "logger.py", "spyware.exe", "spyagent.exe", 
    "spytech.exe", "revealkeylogger.exe", "actualkeylogger.exe", "netbull.exe", "refog.exe",
    "ardamax.exe", "elitekeylogger.exe", "kidlogger.exe", "shadowkeylogger.exe", "realfreekeylogger.exe",
    "microkeylogger.exe", "blackbox.exe", "perfectkeylogger.exe", "hoverwatch.exe",

    # Remote access tools often used for keylogging
    "rat.exe", "darkcomet.exe", "njrat.exe", "remcos.exe", "quasar.exe", "spy_rat.exe",

    # Generic logging patterns
    "keyboardhook.dll", "hook.dll", "keycapture.exe", "inputlogger.exe", "keystroke.exe",
    "logkeys.exe", "syslogger.exe", "recordkeys.exe", "userinput.exe", "activitymonitor.exe",
    "keyscan.exe", "typecatcher.exe", "logger32.exe", "cliplogger.exe", "strokerecorder.exe",

    # Obfuscated variants
    "klogg32.exe", "klg32.exe", "svc_key.exe", "svc_hostlog.exe", "svcmon.exe", "sysmon.exe",
    "winhook.exe", "winlogger.exe", "taskhostlog.exe"
]


# Feature Extraction Function
def extract_features(text):
    char_freq = Counter(text)
    most_common_freq = char_freq.most_common(1)[0][1] if char_freq else 0
    return [
        len(text),
        len(set(text)),
        sum(c.isdigit() for c in text),
        sum(c.isalpha() for c in text),
        sum(c.isupper() for c in text),
        sum(c in '!@#$%^&*()_+=[]{}|;:,.<>?/~`' for c in text),
        text.count(' '),
        most_common_freq,
        int(bool(re.search(r'(.)\1{3,}', text)))
    ]

# Log Events
def log_event(event):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {event}\n")

# Terminate suspicious process
def terminate_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        return True
    except Exception:
        return False

# Scan running processes
def scan_processes():
    suspicious = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            pname = proc.info['name'].lower()
            # Check if the process name *contains* any known keylogger name (partial match)
            if any(known in pname for known in known_keyloggers):
                suspicious.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return suspicious


# Streamlit Page Setup
st.set_page_config(page_title="Keylogger Detection", layout="centered")
page = st.sidebar.selectbox("Navigate", ["Home", "Recent Logs", "About Project"])

# Dashboard Counters
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        pass

with open(LOG_FILE, 'r', encoding='utf-8') as f:
    total_logs = len(f.readlines())

# -------------------- Home Page --------------------
if page == "Home":
    st.title("🔐 Keylogger Detection System")
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("📄 Total Keystrokes Scanned", f"{total_logs}")
    col2.metric("🚨 Total Threats Detected", f"{total_logs}")
    st.markdown("---")

    user_input = st.text_area("Enter Keystrokes for Analysis", "", height=100)

    if st.button("Analyze Keystrokes"):
        if user_input.strip():
            features = np.array([extract_features(user_input)])
            if features.shape[1] != 9:
                st.error("Feature mismatch with model. Retrain your model with 9 features.")
            else:
                prediction = model.predict(features)
                threat = prediction[0] == -1
                result = "⚠️ Suspicious Keystroke Pattern Detected!" if threat else "✅ Normal Keystrokes"
                st.subheader("Analysis Result:")
                st.write(result)

                if threat:
                    log_event("⚠️ Suspicious keystrokes detected")
                    st.error("🚨 Potential Threat Detected! Avoid entering sensitive data.")
                    st.info("💡 Suggestion: Run antivirus, check processes, avoid untrusted apps.")
                else:
                    st.success("✅ No suspicious behavior found.")

                feature_names = ["Length", "Unique", "Digits", "Letters", "Upper", "Symbols", "Spaces", "Repetition", "Pattern"]
                st.markdown("### Feature Analysis")
                fig, ax = plt.subplots(figsize=(6, 3))
                sns.barplot(x=feature_names, y=features[0], palette="coolwarm", ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)

                st.write("**Extracted Features:**", dict(zip(feature_names, features[0])))
        else:
            st.warning("Please enter some keystrokes.")

# -------------------- Logs Page --------------------
elif page == "Recent Logs":
    st.title("📄 Recent Monitoring Logs")
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = f.readlines()
                for line in logs[-10:]:
                    st.text(line.strip())

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🧹 Clear Logs"):
                    open(LOG_FILE, 'w').close()
                    st.success("Logs cleared successfully.")
            with col2:
                st.download_button("📥 Download Logs", data=''.join(logs), file_name="keylogger_alerts.log")

        except UnicodeDecodeError:
            st.error("Log file encoding issue.")
    else:
        st.info("No logs found.")

# -------------------- Process Page --------------------

# -------------------- About Page --------------------
elif page == "About Project":
    st.title("📘 Project Overview")
    st.markdown("""
    ### Existing System:
    - Manual monitoring of system processes
    - No real-time keystroke analysis
    - Dependent on traditional antivirus

    ### Proposed System:
    - Live keystroke behavior analysis using Isolation Forest
    - Real-time detection of suspicious typing patterns
    - Process scan and termination option
    - Auto-log generation with timestamps
    - Visual representation of suspicious patterns
    - Symbols and whitespace detection for better accuracy

    ### Use Cases:
    - Detect keyloggers in cybersecurity labs
    - Add-on tool for ethical hacking kits
    - Background security in data entry environments

    ### Technologies Used:
    - Python, Streamlit, Sklearn, Pandas, Psutil, Matplotlib, Seaborn
    """)