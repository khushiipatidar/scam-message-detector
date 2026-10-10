import os
import streamlit as st
import joblib

st.set_page_config(page_title="Scam Message Detector", page_icon="🛡️", layout="wide")

# ---------- Text (English / Hindi) ----------
TEXT = {
    "English": {
        "title": "Scam Message Detector",
        "subtitle": "Got a suspicious WhatsApp or SMS message? Paste it here and know in seconds if it is a scam.",
        "badge1": "English", "badge2": "हिन्दी", "badge3": "Hinglish",
        "stat1_n": "3", "stat1_t": "Languages supported",
        "stat2_n": "2 sec", "stat2_t": "Result time",
        "stat3_n": "1930", "stat3_t": "Cyber crime helpline",
        "check_h": "Check a message",
        "label": "Paste the message here",
        "placeholder": "Example: Your KYC has expired, click this link now...",
        "button": "🔍 Check message",
        "empty": "Please paste a message first.",
        "scam": "Likely a SCAM", "maybe": "Suspicious", "ok": "Looks genuine",
        "chance": "Scam probability",
        "adv_scam": "Do not click any link. Do not share your OTP, PIN or bank details. Delete the message.",
        "adv_maybe": "Be careful. Do not click links or share personal details. Verify with the bank or sender directly.",
        "adv_ok": "No scam signs found, but stay alert. Never share your OTP with anyone.",
        "examples": "Try an example",
        "ex1": "KYC scam", "ex2": "Lottery scam", "ex3": "Normal message",
        "common_h": "Common scams to watch for",
        "cs": [
            ("🏦", "Fake KYC / bank alert", "\"Your KYC has expired, update now\" with a link. Banks never ask for details on links."),
            ("🎁", "Lottery and prize", "\"You won 10 lakh, send OTP to claim.\" You cannot win a lottery you never entered."),
            ("📦", "Parcel and customs fee", "\"Your parcel is held, pay a small fee.\" The link steals card details."),
            ("💼", "Work from home jobs", "\"Earn 5000 daily from home.\" They ask for money first and disappear."),
        ],
        "how_h": "How it works",
        "steps": [
            ("1", "Paste", "Copy the message from WhatsApp or SMS and paste it above."),
            ("2", "Analyse", "A machine learning model (TF-IDF + Logistic Regression) reads the words and patterns."),
            ("3", "Result", "You get a verdict, a probability and simple advice on what to do."),
        ],
        "note": "This is only a screening tool and can make mistakes. If in doubt, contact your bank or call the cyber crime helpline 1930.",
        "missing": "scam_model.pkl not found. Run `python train_model.py` first (spam.csv must be in this folder).",
        "foot": "Built for SDG 16: Peace, Justice and Strong Institutions",
    },
    "हिन्दी": {
        "title": "स्कैम मैसेज डिटेक्टर",
        "subtitle": "WhatsApp या SMS पर कोई संदिग्ध मैसेज आया है? उसे यहाँ डालें और कुछ ही सेकंड में जानें कि वह स्कैम है या नहीं।",
        "badge1": "English", "badge2": "हिन्दी", "badge3": "Hinglish",
        "stat1_n": "3", "stat1_t": "भाषाएँ समर्थित",
        "stat2_n": "2 सेकंड", "stat2_t": "नतीजे का समय",
        "stat3_n": "1930", "stat3_t": "साइबर क्राइम हेल्पलाइन",
        "check_h": "मैसेज जाँचें",
        "label": "मैसेज यहाँ पेस्ट करें",
        "placeholder": "उदाहरण: आपका KYC एक्सपायर हो गया है, अभी लिंक पर क्लिक करें...",
        "button": "🔍 मैसेज जाँचें",
        "empty": "पहले कोई मैसेज डालें।",
        "scam": "यह स्कैम हो सकता है", "maybe": "संदिग्ध मैसेज", "ok": "मैसेज सही लगता है",
        "chance": "स्कैम होने की संभावना",
        "adv_scam": "किसी लिंक पर क्लिक न करें। OTP, PIN या बैंक की जानकारी किसी को न बताएँ। मैसेज डिलीट कर दें।",
        "adv_maybe": "सावधान रहें। लिंक पर क्लिक न करें और निजी जानकारी न दें। बैंक या भेजने वाले से सीधे पूछकर पुष्टि करें।",
        "adv_ok": "स्कैम के लक्षण नहीं मिले, फिर भी सतर्क रहें। अपना OTP कभी किसी को न बताएँ।",
        "examples": "उदाहरण आज़माएँ",
        "ex1": "KYC स्कैम", "ex2": "लॉटरी स्कैम", "ex3": "सामान्य मैसेज",
        "common_h": "आम स्कैम जिनसे बचें",
        "cs": [
            ("🏦", "फ़र्ज़ी KYC / बैंक अलर्ट", "\"आपका KYC एक्सपायर हो गया\" और साथ में लिंक। बैंक कभी लिंक पर जानकारी नहीं माँगते।"),
            ("🎁", "लॉटरी और इनाम", "\"आपने 10 लाख जीते, OTP भेजें।\" जिस लॉटरी में आपने भाग ही नहीं लिया, उसे आप जीत नहीं सकते।"),
            ("📦", "पार्सल और कस्टम फ़ीस", "\"आपका पार्सल रुका है, थोड़ी फ़ीस भरें।\" लिंक से कार्ड की जानकारी चोरी होती है।"),
            ("💼", "घर बैठे कमाई", "\"घर बैठे रोज़ 5000 कमाएँ।\" पहले पैसे माँगते हैं और फिर गायब हो जाते हैं।"),
        ],
        "how_h": "यह कैसे काम करता है",
        "steps": [
            ("1", "पेस्ट करें", "WhatsApp या SMS से मैसेज कॉपी करके ऊपर डालें।"),
            ("2", "जाँच", "मशीन लर्निंग मॉडल (TF-IDF + Logistic Regression) शब्दों और पैटर्न को पढ़ता है।"),
            ("3", "नतीजा", "आपको फ़ैसला, संभावना और क्या करना है उसकी सरल सलाह मिलती है।"),
        ],
        "note": "यह सिर्फ़ एक जाँच का टूल है और इसमें गलती हो सकती है। शक होने पर अपने बैंक से संपर्क करें या साइबर क्राइम हेल्पलाइन 1930 पर कॉल करें।",
        "missing": "scam_model.pkl नहीं मिली। पहले `python train_model.py` चलाएँ (spam.csv इसी फ़ोल्डर में होनी चाहिए)।",
        "foot": "SDG 16 के लिए बनाया गया: शांति, न्याय और मज़बूत संस्थाएँ",
    },
}

EXAMPLES = {
    "English": ["Your KYC has expired. Click this link now or your account will be blocked.",
                "Congratulations! You won 10 lakh in a lottery. Share your OTP to claim.",
                "I will reach home in 10 minutes, keep the dinner ready."],
    "हिन्दी": ["आपका KYC एक्सपायर हो गया है। अभी लिंक पर क्लिक करें वरना खाता बंद हो जाएगा।",
               "बधाई हो! आपने 10 लाख की लॉटरी जीती है। इनाम पाने के लिए OTP भेजें।",
               "मैं दस मिनट में घर पहुँच रहा हूँ, खाना तैयार रखना।"],
}

# ---------- CSS ----------
st.markdown("""
<style>
#MainMenu, footer, header [data-testid="stToolbar"], .stDeployButton {display: none !important;}
html, body, [class*="css"] {font-family: "Segoe UI", "Nirmala UI", "Noto Sans Devanagari", Arial, sans-serif;}
.stApp {background: linear-gradient(180deg, #e0ecff 0%, #f5f8ff 40%, #ffffff 100%);}
.block-container {max-width: 1100px; padding-top: 1.5rem; padding-bottom: 2rem;}

.hero {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 55%, #7c3aed 100%);
    color: #fff; padding: 36px 34px; border-radius: 22px;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.30); margin-bottom: 22px;
}
.hero h1 {margin: 0; font-size: 2.4rem; color: #fff; padding: 0; line-height: 1.2;}
.hero p {margin: 10px 0 14px 0; font-size: 1.1rem; opacity: 0.95; color: #fff; max-width: 720px;}
.badge {display: inline-block; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.4);
        color: #fff; padding: 4px 14px; border-radius: 999px; margin-right: 8px; font-size: 0.9rem;}

.stat {background: #fff; border-radius: 16px; padding: 18px; text-align: center;
       box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08); border-top: 4px solid #2563eb;}
.stat .n {font-size: 1.9rem; font-weight: 800; color: #1e3a8a;}
.stat .t {font-size: 0.9rem; color: #64748b;}

.section-h {font-size: 1.4rem; font-weight: 700; color: #1e293b; margin: 26px 0 12px 0;}

.card {background: #fff; border-radius: 16px; padding: 18px 20px; height: 100%;
       box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08); margin-bottom: 14px;}
.card .ic {font-size: 1.8rem;}
.card h4 {margin: 6px 0 4px 0; color: #1e293b; font-size: 1.05rem;}
.card p {margin: 0; color: #475569; font-size: 0.93rem;}

.step {background: #fff; border-radius: 16px; padding: 18px 20px;
       box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08); border-left: 6px solid #7c3aed;}
.step .num {display: inline-block; width: 32px; height: 32px; line-height: 32px; text-align: center;
            border-radius: 50%; background: #7c3aed; color: #fff; font-weight: 700; margin-right: 8px;}
.step b {font-size: 1.05rem; color: #1e293b;}
.step p {margin: 8px 0 0 0; color: #475569; font-size: 0.93rem;}

.checkbox-wrap {background: #fff; border-radius: 18px; padding: 22px 24px;
                box-shadow: 0 6px 20px rgba(15, 23, 42, 0.10);}
textarea {border-radius: 12px !important; font-size: 1.02rem !important;}

.stButton > button {border-radius: 10px; border: 1px solid #2563eb; font-weight: 600; transition: all 0.15s ease;}
.stButton > button[kind="primary"] {background: linear-gradient(135deg, #2563eb, #7c3aed); color: #fff;
                                    border: none; width: 100%; padding: 0.7rem 0; font-size: 1.05rem;}
.stButton > button:hover {transform: translateY(-1px); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);}

.result {border-radius: 14px; padding: 18px 20px; margin-top: 14px; border-left: 8px solid;}
.result h3 {margin: 0 0 6px 0; font-size: 1.4rem;}
.result p {margin: 4px 0; font-size: 1rem;}
.r-scam  {background: #fef2f2; border-color: #dc2626; color: #7f1d1d;}
.r-maybe {background: #fffbeb; border-color: #f59e0b; color: #78350f;}
.r-ok    {background: #f0fdf4; border-color: #16a34a; color: #14532d;}

.note {font-size: 0.85rem; color: #64748b; margin-top: 16px;}
.foot {text-align: center; font-size: 0.85rem; color: #94a3b8; margin-top: 34px;}
</style>
""", unsafe_allow_html=True)

# ---------- Language switch ----------
lang = st.radio("🌐", list(TEXT.keys()), horizontal=True, label_visibility="collapsed")
T = TEXT[lang]

# ---------- Hero ----------
st.markdown(f"""
<div class="hero">
  <h1>🛡️ {T['title']}</h1>
  <p>{T['subtitle']}</p>
  <span class="badge">{T['badge1']}</span><span class="badge">{T['badge2']}</span><span class="badge">{T['badge3']}</span>
</div>
""", unsafe_allow_html=True)

# ---------- Stats ----------
s1, s2, s3 = st.columns(3)
for col, n, t in ((s1, T["stat1_n"], T["stat1_t"]), (s2, T["stat2_n"], T["stat2_t"]), (s3, T["stat3_n"], T["stat3_t"])):
    col.markdown(f'<div class="stat"><div class="n">{n}</div><div class="t">{t}</div></div>', unsafe_allow_html=True)

# ---------- Model ----------
if not os.path.exists("scam_model.pkl"):
    st.error(T["missing"])
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load("scam_model.pkl")

model = load_model()

# ---------- Checker ----------
st.markdown(f'<div class="section-h">{T["check_h"]}</div>', unsafe_allow_html=True)

def set_example(text):
    st.session_state["msg"] = text

st.write(f"**{T['examples']}**")
c1, c2, c3 = st.columns(3)
for col, name, text in zip((c1, c2, c3), (T["ex1"], T["ex2"], T["ex3"]), EXAMPLES[lang]):
    col.button(name, on_click=set_example, args=(text,), use_container_width=True, key=f"{lang}-{name}")

msg = st.text_area(T["label"], key="msg", height=150, placeholder=T["placeholder"])

if st.button(T["button"], type="primary"):
    if not msg.strip():
        st.warning(T["empty"])
    else:
        prob = float(model.predict_proba([msg.lower()])[0][1])
        if prob >= 0.5:
            cls, icon, head, adv = "r-scam", "🚨", T["scam"], T["adv_scam"]
        elif prob >= 0.3:
            cls, icon, head, adv = "r-maybe", "⚠️", T["maybe"], T["adv_maybe"]
        else:
            cls, icon, head, adv = "r-ok", "✅", T["ok"], T["adv_ok"]
        st.markdown(f"""
        <div class="result {cls}">
          <h3>{icon} {head}</h3>
          <p><b>{T['chance']}:</b> {prob*100:.1f}%</p>
          <p>{adv}</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(max(prob, 0.0), 1.0))

st.markdown(f'<div class="note">{T["note"]}</div>', unsafe_allow_html=True)

# ---------- Common scams ----------
st.markdown(f'<div class="section-h">{T["common_h"]}</div>', unsafe_allow_html=True)
row1 = st.columns(2)
row2 = st.columns(2)
for col, (ic, h, p) in zip(row1 + row2, T["cs"]):
    col.markdown(f'<div class="card"><div class="ic">{ic}</div><h4>{h}</h4><p>{p}</p></div>', unsafe_allow_html=True)

# ---------- How it works ----------
st.markdown(f'<div class="section-h">{T["how_h"]}</div>', unsafe_allow_html=True)
h1, h2, h3 = st.columns(3)
for col, (n, h, p) in zip((h1, h2, h3), T["steps"]):
    col.markdown(f'<div class="step"><span class="num">{n}</span><b>{h}</b><p>{p}</p></div>', unsafe_allow_html=True)

st.markdown(f'<div class="foot">{T["foot"]}</div>', unsafe_allow_html=True)
