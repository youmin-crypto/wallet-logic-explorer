import streamlit as st
from mnemonic import Mnemonic
import binascii
from eth_utils import to_checksum_address
from eth_keys import keys

st.set_page_config(page_title="Crypto Wallet Logic Explorer", layout="wide")

st.title("🔐 Crypto Wallet Generator & Logic Explorer")
st.write("Seed Phrase (Mnemonic) ကနေ Wallet Address တစ်ခု ဘယ်လိုဖြစ်လာသလဲဆိုတာကို လေ့လာကြမယ်။")

# ၁။ Entropy (ကျပန်း အချက်အလက်) ဖန်တီးခြင်း
st.subheader("အဆင့် (၁) - Entropy (ကျပန်းဂဏန်းများ)")
st.info("Wallet တစ်ခုရဲ့ အစဟာ ခန့်မှန်းလို့မရတဲ့ ကျပန်းဂဏန်းတွေ (Randomness) ကနေ စတင်ပါတယ်။")

if st.button("Wallet အသစ်တစ်ခု စတင်တည်ဆောက်မည်"):
    # Generate 128-bit entropy
    mnemo = Mnemonic("english")
    entropy = mnemo.generate(strength=128) # 12 words seed phrase
    
    st.session_state.seed_phrase = entropy
    # Convert seed phrase back to hex for showing entropy
    st.session_state.entropy_hex = binascii.hexlify(mnemo.to_entropy(entropy)).decode()

if 'seed_phrase' in st.session_state:
    st.code(f"Entropy (Hex): {st.session_state.entropy_hex}")
    
    # ၂။ Mnemonic (Seed Phrase)
    st.subheader("အဆင့် (၂) - Seed Phrase (Mnemonic)")
    st.warning("ဒီ ၁၂ လုံးသော စကားလုံးဟာ သင့်ပိုင်ဆိုင်မှုအားလုံးရဲ့ သော့ချက်ပါ။ ဘယ်သူ့ကိုမှ မပေးရပါဘူး။")
    st.success(f"**Seed Phrase:** {st.session_state.seed_phrase}")
    
    # ၃။ Private Key & Public Key
    st.subheader("အဆင့် (၃) - Keys Generation")
    
    # အလွယ်ဆုံးပြရန်အတွက် Seed ကိုသုံးပြီး Private Key တစ်ခု ထုတ်ပြခြင်း
    seed_bytes = Mnemonic.to_seed(st.session_state.seed_phrase)
    # Ethereum-style key generation (Simplified for learning)
    priv_key_bytes = seed_bytes[:32]
    priv_key = keys.PrivateKey(priv_key_bytes)
    pub_key = priv_key.public_key
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Private Key (လျှို့ဝှက်ကုဒ်)**")
        st.code(priv_key, language='text')
        st.caption("ဒါက ငွေထုတ်ဖို့သုံးတဲ့ သော့ပါ။")
        
    with col2:
        st.write("**Public Key (အများမြင်ကုဒ်)**")
        st.code(pub_key, language='text')
        st.caption("ဒါက Private Key ကနေ သင်္ချာနည်းအရ တွက်ထုတ်ထားတာပါ။")

    # ၄။ Wallet Address
    st.subheader("အဆင့် (၄) - Wallet Address")
    address = pub_key.to_checksum_address()
    st.info(f"**Public Address (သင့်ရဲ့ လိပ်စာ):** {address}")
    st.write("ဒီ address ကိုတော့ သူများဆီက ငွေလက်ခံဖို့အတွက် ပေးလို့ရပါတယ်။")
