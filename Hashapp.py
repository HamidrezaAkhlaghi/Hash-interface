import streamlit as st
import hashlib
import time
import base64
import os
from supabase import create_client, Client

# --- SETUP & CONFIG ---
st.set_page_config(page_title="ABDI Coin Network", page_icon="🪙", layout="wide")

# --- IMAGE ENCODING FOR UI ---
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Read the local image file verbatim
coin_b64 = get_image_base64("OIP_2.webp")

# --- PREMIUM CSS UI DESIGN ---
page_bg_img = f"""
<style>
/* Import premium minimalist fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* High-End Dark Background with Image Overlay */
[data-testid="stAppViewContainer"] {{
    background-color: #09090b;
    background-image: 
        linear-gradient(rgba(9, 9, 11, 0.85), rgba(9, 9, 11, 0.95)),
        url('data:image/webp;base64,{coin_b64}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #e4e4e7;
    font-family: 'Inter', sans-serif;
}}

/* Hide standard header */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

/* 3D Floating Interactive Image */
.coin-wrapper {{
    position: fixed;
    top: 40px;
    right: 50px;
    width: 140px;
    height: 140px;
    z-index: 999;
    perspective: 1200px;
    animation: floatCoin 4s ease-in-out infinite;
}}

.coin-3d {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
    background-image: url('data:image/webp;base64,{coin_b64}');
    background-size: cover;
    background-position: center;
    box-shadow: 
        0 10px 30px rgba(0, 0, 0, 0.9),
        0 0 25px rgba(212, 175, 55, 0.2),
        inset 0 0 20px rgba(255, 255, 255, 0.1);
    /* Continuous slow rotation */
    animation: spinCoin 15s linear infinite;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}}

/* Interactive reaction on hover - Speeds up, glows gold */
.coin-3d:hover {{
    animation: spinCoin 2s linear infinite;
    box-shadow: 
        0 0 50px rgba(212, 175, 55, 0.6), 
        inset 0 0 30px rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
}}

@keyframes spinCoin {{
    0% {{ transform: rotateY(0deg); }}
    100% {{ transform: rotateY(360deg); }}
}}

@keyframes floatCoin {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-12px); }}
}}

/* Typography */
.main-title {{
    color: #ffffff;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 4em;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 5px;
    background: linear-gradient(90deg, #d4af37, #ffffff, #d4af37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s infinite linear;
    background-size: 200% auto;
}}

@keyframes shimmer {{
    to {{ background-position: 200% center; }}
}}

.sub-title {{
    color: #a1a1aa;
    text-align: center;
    margin-bottom: 50px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1em;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* Sleek Block Cards */
.block-card {{
    background: rgba(24, 24, 27, 0.5);
    border: 1px solid rgba(212, 175, 55, 0.15);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}}

/* Subtle lifting hover effect */
.block-card:hover {{
    transform: translateY(-6px);
    border: 1px solid rgba(212, 175, 55, 0.5);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7), 0 0 20px rgba(212, 175, 55, 0.1);
}}

.block-header {{
    color: #d4af37;
    border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    padding-bottom: 12px;
    margin-bottom: 16px;
    font-family: 'Inter', sans-serif;
    font-size: 1.3em;
    font-weight: 800;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

/* Hash Text Styling */
.hash-text {{
    font-family: 'JetBrains Mono', monospace;
    color: #fde047;
    word-wrap: break-word;
    font-size: 0.85em;
    background: rgba(0, 0, 0, 0.6);
    padding: 6px 12px;
    border-radius: 6px;
    border-left: 3px solid #d4af37;
    display: inline-block;
    margin-top: 4px;
    letter-spacing: 0.5px;
}}

/* Streamlit Native Element Overrides */
div.stButton > button {{
    background: linear-gradient(135deg, #d4af37, #b8860b);
    color: #09090b !important;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 1.1em;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}}

div.stButton > button:hover {{
    background: linear-gradient(135deg, #fde047, #d4af37);
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5);
}}

.stTextArea textarea {{
    background-color: rgba(9, 9, 11, 0.7) !important;
    color: #fde047 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}}

.stTextArea textarea:focus {{
    border: 1px solid #d4af37 !important;
    box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.3) !important;
}}
</style>

<!-- Floating Image Component -->
<div class="coin-wrapper">
    <div class="coin-3d"></div>
</div>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- SUPABASE CONNECTION ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- BLOCKCHAIN FUNCTIONS ---
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
            "data": "Genesis Block - ABDI Coin Mainnet Initialized",
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
        
        if nonce % 10000 == 0:
            mining_placeholder.info(f"⚙️ Mining ABDI Block... Nonce: `{nonce}` | Current: `{new_hash[:12]}...`")
            
        if new_hash.startswith(target):
            mining_placeholder.success(f"✓ ABDI Block Verified. Nonce: `{nonce}`")
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
st.markdown('<div class="main-title">ABDI COIN</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Next-Generation Decentralized Ledger Protocol ($ABDI)</div>', unsafe_allow_html=True)

# Transaction Input Form
st.markdown("<h4 style='color: #e4e4e7; font-weight: 600; margin-bottom: 1rem;'>Inject Transaction</h4>", unsafe_allow_html=True)
with st.container():
    data_input = st.text_area("Enter ABDI Smart Contract or Payload:", height=100, placeholder="Execute transfer: 500 $ABDI to Wallet 0x...")
    if st.button("Sign & Mine Block ⛏️", use_container_width=True):
        if data_input:
            add_block(data_input)
            st.rerun() 
        else:
            st.warning("⚠️ Payload cannot be empty.")

st.markdown("<br><hr style='border: 0; height: 1px; background: rgba(212, 175, 55, 0.2); margin: 2rem 0;'><br>", unsafe_allow_html=True)

# Display the Blockchain
st.markdown("<h4 style='color: #e4e4e7; font-weight: 600; margin-bottom: 1rem;'>ABDI Mainnet Ledger</h4>", unsafe_allow_html=True)
blockchain_data = sync_with_supabase()

for block in reversed(blockchain_data):
    st.markdown(f"""
    <div class="block-card">
        <div class="block-header">
            <span>Block #{block['index']}</span>
            <span style="font-size: 0.8em; color: #a1a1aa; font-family: 'JetBrains Mono', monospace; font-weight: 400;">{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block['timestamp']))}</span>
        </div>
        <div style="margin-bottom: 16px;">
            <span style="color: #a1a1aa; font-size: 0.9em; text-transform: uppercase; font-weight: 600;">Payload Data</span><br>
            <span style="color: #ffffff; font-family: 'JetBrains Mono', monospace; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 6px; display: inline-block; width: 100%; margin-top: 6px;">{block['data']}</span>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 16px;">
            <div>
                <span style="color: #a1a1aa; font-size: 0.8em; text-transform: uppercase; font-weight: 600;">Nonce</span><br>
                <span class="hash-text" style="color: #ffffff;">{block.get('nonce', 0)}</span>
            </div>
            <div>
                <span style="color: #a1a1aa; font-size: 0.8em; text-transform: uppercase; font-weight: 600;">Previous Hash</span><br>
                <span class="hash-text">{block['previous_hash'][:16]}...{block['previous_hash'][-8:]}</span>
            </div>
        </div>
        
        <div>
            <span style="color: #a1a1aa; font-size: 0.8em; text-transform: uppercase; font-weight: 600;">Block Hash</span><br>
            <span class="hash-text" style="border-left: 3px solid #d4af37; color: #d4af37; font-weight: bold; width: 100%; box-sizing: border-box;">{block['hash']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
