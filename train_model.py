"""
Scam / Fake Message Detector - model training.

Zaroorat: is folder me spam.csv (Kaggle: SMS Spam Collection Dataset) rakho.
Chalane ka tareeka:  python train_model.py
Output: scam_model.pkl
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# 1. English data (spam.csv). Kaggle ke alag versions me column names alag hote hain.
raw = pd.read_csv("spam.csv", encoding="latin-1")
if {"v1", "v2"}.issubset(raw.columns):
    df1 = raw[["v1", "v2"]]
elif {"Category", "Message"}.issubset(raw.columns):
    df1 = raw[["Category", "Message"]]
else:
    raise SystemExit(f"spam.csv ke columns samajh nahi aaye: {list(raw.columns)}")
df1.columns = ["label", "text"]

# 2. Hindi / Hinglish data
df2 = pd.read_csv("hindi.csv", encoding="utf-8")

# 3. Jodo aur clean karo
df = pd.concat([df1, df2], ignore_index=True)
df["label"] = df["label"].map({"ham": 0, "spam": 1})
df = df.dropna(subset=["label", "text"])
df["text"] = df["text"].astype(str).str.lower()
print("Label counts:\n", df["label"].value_counts(), "\n")

# 4. Split
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# 5. Model
model = Pipeline([
    # token_pattern: Devanagari (matras) ko bhi sahi se pakadne ke liye
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000,
                              token_pattern=r"(?u)[\w\u0900-\u097F]+")),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
model.fit(X_train, y_train)

# 6. Result
pred = model.predict(X_test)
print(classification_report(y_test, pred))
print("Confusion matrix:\n", confusion_matrix(y_test, pred))

# 7. Save
joblib.dump(model, "scam_model.pkl")
print("\nscam_model.pkl save ho gayi.")
