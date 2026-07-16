import streamlit as st
import hashlib
import time
import base64
import os
from supabase import create_client, Client

# --- SETUP & CONFIG ---
st.set_page_config(page_title="ABDI Network", page_icon="🪙", layout="centered")

# --- IMAGE ENCODING FOR UI ---
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

coin_b64 = get_image_base64("OIP_2.webp")

# --- ELEGANT & IMMERSIVE CSS + JS ---
page_bg_img = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&family=Playfair+Display:wght@700&family=Fira+Code:wght@400;500&display=swap');

[data-testid="stAppViewContainer"] {{
    background-color: #0a0a0a;
    background-image: 
        radial-gradient(circle at 50% 20%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
        linear-gradient(rgba(10, 10, 10, 0.92), rgba(10, 10, 10, 0.96)),
        url('data:image/webp;base64,{coin_b64}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ededed;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
}}

/* Floating animated coin */
.floating-coin {{
    position: fixed;
    top: 80px;
    right: 60px;
    width: 120px;
    height: 120px;
    z-index: 1000;
    transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    filter: drop-shadow(0 25px 35px rgba(212, 175, 55, 0.4));
}}

.floating-coin:hover {{
    transform: scale(1.15) rotate(12deg);
}}

/* Global glow effects */
.glow-gold {{
    text-shadow: 0 0 20px rgba(212, 175, 55, 0.6),
                 0 0 40px rgba(212, 175, 55, 0.3);
}}

/* Hide header */
[data-testid="stHeader"] {{
    background: transparent;
}}

/* Elegant Typography */
.main-title {{
    font-family: 'Playfair Display', serif;
    font-size: 3.4rem;
    font-weight: 700;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #ffffff, #d4af37, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.1rem;
    animation: title-shimmer 6s linear infinite;
}}

@keyframes title-shimmer {{
    0% {{ background-position: 0% 50%; }}
    100% {{ background-position: 200% 50%; }}
}}

.sub-title {{
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    font-weight: 300;
    color: #a1a1aa;
    text-align: center;
    margin-bottom: 3.5rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}}

/* Premium Glass Cards */
.glass-card {{
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(212, 175, 55, 0.15);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    position: relative;
    overflow: hidden;
}}

.glass-card::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 40%;
    height: 40%;
    background: radial-gradient(circle, rgba(212,175,55,0.2) 0%, transparent 70%);
    opacity: 0;
    transition: all 0.6s ease;
}}

.glass-card:hover {{
    transform: translateY(-8px);
    border-color: #d4af37;
    box-shadow: 0 25px 50px rgba(212, 175, 55, 0.15);
}}

.glass-card:hover::before {{
    opacity: 1;
    transform: translate(80%, 80%);
}}

/* Block header */
.block-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(212, 175, 55, 0.15);
    padding-bottom: 16px;
    margin-bottom: 20px;
}}

.block-id {{
    font-size: 1.35rem;
    font-weight: 600;
    color: #d4af37;
    letter-spacing: -0.5px;
}}

.block-time {{
    font-size: 0.85rem;
    color: #71717a;
    font-family: 'Fira Code', monospace;
}}

/* Labels & Data */
.data-label {{
    font-size: 0.73rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #888888;
    margin-bottom: 6px;
    display: block;
}}

.mono-text {{
    font-family: 'Fira Code', monospace;
    font-size: 0.9rem;
    color: #d4d4d8;
    line-height: 1.5;
    word-break: break-all;
}}

/* Input Area */
.stTextArea textarea {{
    background-color: rgba(20, 20, 20, 0.7) !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
    color: #ededed !important;
    font-family: 'Fira Code', monospace !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: all 0.3s ease;
}}

.stTextArea textarea:focus {{
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15) !important;
}}

/* Button */
div.stButton > button {{
    background: linear-gradient(90deg, #d4af37, #f0d48f);
    color: #111111 !important;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    border-radius: 50px;
    border: none;
    padding: 14px 42px;
    font-size: 1.05rem;
    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
}}

div.stButton > button:hover {{
    transform: translateY(-3px) scale(1.03);
    box-shadow: 0 20px 40px rgba(212, 175, 55, 0.4);
    background: linear-gradient(90deg, #f0d48f, #d4af37);
}}

/* Subtle scanline / luxury effect */
body::after {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: repeating-linear-gradient(
        transparent 0px,
        transparent 2px,
        rgba(255,255,255,0.015) 2px,
        rgba(255,255,255,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}}
</style>

<script>
document.addEventListener('mousemove', function(e) {{
    const coin = document.getElementById('floating-coin');
    if (coin) {{
        const x = (e.clientX / window.innerWidth - 0.5) * 25;
        const y = (e.clientY / window.innerHeight - 0.5) * 25;
        coin.style.transform = `perspective(1000px) rotateY(${{x}}deg) rotateX(${{-y}}deg)`;
    }}
}});
</script>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# --- SUPABASE CONNECTION ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- BLOCKCHAIN FUNCTIONS (unchanged) ---
def hash_block(index, previous_hash, timestamp, data, nonce):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(nonce)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def sync_with_supabase():
    response = supabase.table("blocks").select("*").order("index").execute()
    if not response.data:
        genesis_block = {
            "index": 0,
            "previous_hash": "0",
            "timestamp": time.time(),
            "data": "Network Genesis",
            "nonce": 0
        }
        genesis_block["hash"] = hash_block(
            genesis_block["index"], genesis_block["previous_hash"],
            genesis_block["timestamp"], genesis_block["data"], genesis_block["nonce"]
        )
        supabase.table("blocks").insert(genesis_block).execute()
        return [genesis_block]
    return response.data

def add_block(data):
    chain = sync_with_supabase()
    last_block = chain[-1]
   
    new_index = last_block["index"] + 1
    previous_hash = last_block["hash"]
    timestamp = time.time()
   
    nonce = 0
    difficulty = 4
    target = "0" * difficulty
   
    mining_placeholder = st.empty()
   
    while True:
        new_hash = hash_block(new_index, previous_hash, timestamp, data, nonce)
       
        if nonce % 8000 == 0:
            mining_placeholder.info(f"⛏️ Mining Block... Nonce: {nonce:,}")
           
        if new_hash.startswith(target):
            mining_placeholder.success("✅ Block mined & verified successfully")
            time.sleep(1.2)
            break
        nonce += 1
    new_block = {
        "index": new_index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "data": data,
        "nonce": nonce,
        "hash": new_hash
    }
   
    supabase.table("blocks").insert(new_block).execute()

# --- UI LAYOUT ---
st.markdown('<div class="main-title glow-gold">ABDI COIN</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Immutable • Elegant • Yours</div>', unsafe_allow_html=True)

# Floating Interactive Coin
st.markdown(f"""
<div id="floating-coin" class="floating-coin">
    <img src="data:image/webp;base64,{coin_b64}" width="120" height="120" style="border-radius: 50%; border: 3px solid #d4af37;">
</div>
""", unsafe_allow_html=True)

# Transaction Entry
with st.container():
    st.markdown('<span class="data-label">NEW TRANSACTION PAYLOAD</span>', unsafe_allow_html=True)
    data_input = st.text_area(
        "Payload", 
        height=130, 
        label_visibility="collapsed", 
        placeholder="Describe your transfer, smart contract, or message..."
    )
   
    if st.button("Sign & Mine Block", use_container_width=True):
        if data_input.strip():
            add_block(data_input.strip())
            st.rerun()
        else:
            st.warning("Please enter a payload before mining.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<span class="data-label" style="font-size: 1rem; text-align:center; display:block;">LIVE NETWORK LEDGER</span>', unsafe_allow_html=True)

# Ledger Rendering
blockchain_data = sync_with_supabase()
for block in reversed(blockchain_data):
    timestamp_str = time.strftime('%b %d, %Y • %H:%M:%S', time.localtime(block['timestamp']))
    st.markdown(f"""
    <div class="glass-card">
        <div class="block-header">
            <span class="block-id">BLOCK {block['index']}</span>
            <span class="block-time">{timestamp_str}</span>
        </div>
       
        <div style="margin-bottom: 20px;">
            <span class="data-label">PAYLOAD</span>
            <span class="mono-text" style="color: #ffffff; font-size: 1rem;">{block['data']}</span>
        </div>
       
        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 32px; margin-bottom: 20px;">
            <div>
                <span class="data-label">NONCE</span>
                <span class="mono-text" style="font-size: 1.1rem;">{block.get('nonce', 0):,}</span>
            </div>
            <div>
                <span class="data-label">PREVIOUS HASH</span>
                <span class="mono-text" style="font-size: 0.85rem;">{block['previous_hash']}</span>
            </div>
        </div>
       
        <div>
            <span class="data-label">BLOCK HASH</span>
            <span class="mono-text" style="color: #d4af37; font-size: 0.85rem; word-break: break-all;">{block['hash']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
