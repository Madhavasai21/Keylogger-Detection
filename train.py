import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from collections import Counter
import re

# Load dataset
df = pd.read_csv("keylogger_dataset.csv")

# Feature extraction function
def extract_features(text):
    char_freq = Counter(text)
    most_common_freq = char_freq.most_common(1)[0][1] if char_freq else 0
    return [
        len(text),
        len(set(text)),
        sum(c.isdigit() for c in text),
        sum(c.isalpha() for c in text),
        sum(c.isupper() for c in text),
        sum(c in "!@#$%^&*()" for c in text),       # Special symbol count
        most_common_freq,
        text.count(" "),                            # Space count
        int(bool(re.search(r'(.)\1{2,}', text)))     # Pattern repetition
    ]

# Extract features
df["features"] = df["Keystrokes"].apply(extract_features)
X = np.array(df["features"].tolist())
y = df["Label"]  # Assumes labels are 0 = suspicious, 1 = normal

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("✅ Classification Report:\n", classification_report(y_test, y_pred))
print("✅ Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model
joblib.dump(model, "keylogger_model.pkl")
print("✅ Trained model saved as 'keylogger_model.pkl'")
