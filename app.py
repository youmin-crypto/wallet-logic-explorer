import streamlit as st
from mnemonic import Mnemonic
import binascii
from eth_utils import to_checksum_address
from eth_keys import keys

# Page Settings
st.set_page_config(page_title="Crypto Wallet Pro Explorer", layout="wide")

# --- CUSTOM CSS (ဒါက Website ကို လှအောင်လုပ်ပေးမှာပါ) ---
st.markdown("""
    <style>
    /* Background တစ်ခုလုံးကို Dark Mode လုပ်မယ် */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    /* ခလုတ်တွေကို Neon Green အရောင်ပြောင်းမယ် */
    div.stButton > button:first-child {
        background-color: #00FF41;
        color: black;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 0 15px #00FF41;
    }
    div.stButton > button:hover {
        background-color: #008F11;
        box-shadow: 0 0 25px #00FF41;
        color: white;
    }
    /* Card ပုံစံ Box လေးတွေ */
    .step-box {
        background-color: #1A1C24;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00FF41;
        margin-bottom: 20px;
    }
    /* Address ပြတဲ့ box ကို ထူးခြားအောင်လုပ်မယ် */
    .address-box {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔐 Crypto Wallet Generator (Pro Version)")
st.write("နည်းပညာအမြင်နဲ့ Wallet တစ်ခုကို အူစုံသဲစုံ လေ့လာကြည့်ကြမယ်။")

# Sidebar
with st.sidebar:
    st.header("🛠️ Settings")
    st.info("ဤ Tool သည် ပညာပေးရန် သက်သက်သာ ဖြစ်ပါသည်။")
    if st.button("🔄 Reset / New Wallet"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# Logic
if st.button("✨ အသစ်စက်စက် Wallet တစ်ခု တည်ဆောက်မည်"):
    mnemo = Mnemonic("english")
    entropy = mnemo.generate(strength=128)
    st.session_state.seed_phrase = entropy
    st.session_state.entropy_hex = binascii.hexlify(mnemo.to_entropy(entropy)).decode()

if 'seed_phrase' in st.session_state:
    # အဆင့် ၁
    st.markdown(f'<div class="step-box"><h3>အဆင့် (၁) - Entropy (Hex)</h3><code>{st.session_state.entropy_hex}</code></div>', unsafe_allow_html=True)
    
    # အဆင့် ၂
    st.markdown(f'<div class="step-box"><h3>အဆင့် (၂) - Seed Phrase</h3><p style="color: #00FF41; font-size: 1.2rem;">{st.session_state.seed_phrase}</p></div>', unsafe_allow_html=True)
    
    # အဆင့် ၃ - Keys
    seed_bytes = Mnemonic.to_seed(st.session_state.seed_phrase)
    priv_key_bytes = seed_bytes[:32]
    priv_key = keys.PrivateKey(priv_key_bytes)
    pub_key = priv_key.public_key
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="step-box"><h4>Private Key</h4>', unsafe_allow_html=True)
        st.code(priv_key)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="step-box"><h4>Public Key</h4>', unsafe_allow_html=True)
        st.code(pub_key)
        st.markdown('</div>', unsafe_allow_html=True)

    # အဆင့် ၄ - Address
    address = pub_key.to_checksum_address()
    st.markdown("<h3>အဆင့် (၄) - Final Wallet Address</h3>", unsafe_allow_html=True)
    st.markdown(f'<div class="address-box">{address}</div>', unsafe_allow_html=True)
    st.balloons()
