# predict.py
import joblib
from features import extract_features

# Load model
model = joblib.load('model.pkl')

# User input
url = input("Enter a URL to check: ").strip()
if not url.startswith("http"):
    url = "http://" + url

# Feature extraction
features = extract_features(url)
prediction = model.predict([features])[0]

# Final output
if prediction == 1:
    print("⚠️  Final Verdict: This URL is likely a PHISHING site.")
else:
    print("✅  Final Verdict: This URL seems legitimate.")
