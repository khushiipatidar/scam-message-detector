# Scam / Fake Message Detector (SDG 16)

WhatsApp / SMS message paste karo, model batata hai Scam ya Genuine (confidence % ke saath).
Hindi, English aur Hinglish support. Model: TF-IDF + Logistic Regression.

## Files
- `app.py` - Streamlit demo
- `train_model.py` - model training script
- `hindi.csv` - Hindi/Hinglish scam aur genuine messages (36 rows)
- `requirements.txt` - libraries

## Chalane ke steps
1. `pip install -r requirements.txt`
2. Kaggle se "SMS Spam Collection Dataset" download karke `spam.csv` is folder me rakho.
3. `python train_model.py`  (isse `scam_model.pkl` banegi)
4. `streamlit run app.py`

Agar Colab se pehle hi `scam_model.pkl` bana li hai, to use is folder me copy karo aur seedha step 4 chalao.

## Limitations (presentation me zaroor batao)
- Training data zyadatar English hai, Hindi data kam hai, isliye Hindi scams kabhi kabhi miss ho sakte hain.
- Naye tarah ke scams model ko pehle se nahi pata.
- Ye sirf screening tool hai, final faisla nahi.
