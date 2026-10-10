# Scam / Fake Message Detector

Detects scam WhatsApp and SMS messages in **English, Hindi and Hinglish** using machine learning.
Paste a message, get a verdict (Scam, Suspicious or Genuine), a probability and simple advice.

Built for **SDG 16: Peace, Justice and Strong Institutions**.

## Features

- Text classification with **TF-IDF + Logistic Regression** (fast, no GPU needed)
- Understands English, Hinglish (Roman script) and Hindi (Devanagari script)
- Streamlit web app with an English / हिन्दी language switch
- Three-level result: Scam (50% and above), Suspicious (30% to 50%), Genuine (below 30%)
- Safety advice with each result and the cyber crime helpline (1930, India)

## Results

Evaluated on a held-out test set of 1,126 messages (20% of the data).

| Metric | Value |
|---|---|
| Accuracy | 98% |
| Precision (scam) | 0.94 |
| Recall (scam) | 0.95 |

Confusion matrix:

| | Predicted genuine | Predicted scam |
|---|---|---|
| **Actually genuine** | 961 | 10 |
| **Actually scam** | 8 | 147 |

The first model (Naive Bayes, 20 Hindi messages) had a scam recall of 0.81. Adding more Hindi/Hinglish data and using balanced class weights raised it to 0.95.

## Data

- **English:** [SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) (5,572 messages). The file `spam.csv` is not included in this repository. Download it from Kaggle.
- **Hindi and Hinglish:** `hindi.csv`, 56 messages written for this project (30 scam, 26 genuine, 20 of them in Devanagari script).

## Run the demo

The trained model `scam_model.pkl` is included, so the app runs directly.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

## Train the model again

1. Download `spam.csv` from Kaggle and put it in this folder.
2. Run:

```bash
python train_model.py
```

This prints the accuracy, precision, recall and confusion matrix, and saves a new `scam_model.pkl`.

## Project files

| File | Purpose |
|---|---|
| `app.py` | Streamlit web app |
| `train_model.py` | Trains and saves the model |
| `hindi.csv` | Hindi and Hinglish training messages |
| `scam_model.pkl` | Trained model |
| `requirements.txt` | Python libraries (scikit-learn is pinned to match the saved model) |

## Limitations

- Only 56 Hindi and Hinglish messages, so Hindi results are less reliable than English.
- The English dataset is older and does not include the newest scam styles.
- The model reads words only. It does not check links, sender numbers or images.
- It is a screening tool and can make mistakes. 10 of 971 genuine test messages were flagged as scams.

## Future work

- A larger Hindi and Hinglish dataset collected from real reports
- A WhatsApp or Telegram bot for one-tap checks
- A multilingual BERT model
- Link and sender checks

## Disclaimer

This tool gives a probability, not proof. If a message looks suspicious, do not click links or share your OTP, and contact your bank. In India, report cyber fraud on **1930**.
