# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from features import extract_features

# Load the simplified dataset
df = pd.read_csv('phish_dataset_simple.csv')

# Extract features for each URL
X = df['url'].apply(lambda url: extract_features(url)).tolist()

# Convert labels to binary
y = df['status'].map({'legitimate': 0, 'phishing': 1})

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, 'model.pkl')
print("✅ Model saved to model.pkl")
