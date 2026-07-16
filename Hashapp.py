import streamlit as st
import hashlib
import time
import base64
import os
from supabase import create_client, Client

# --- SETUP & CONFIG ---
st.set_page_config(page_title="HamiZex Blockchain", page_icon="🪙", layout="wide")

# --- IMAGE ENCODING FOR UI ---
# Dynamically load the requested local image to bypass Streamlit static folder limits
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Reference the file verbatim as requested
coin_b64 = get_image_base64("OIP.webp")

# --- PREMIUM CSS UI DESIGN (Sleek, High-End Dark Mode) ---
page_bg_img = f"""
<style>
/* Import premium minimalist fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* High-End Dark Background */
[data-testid="stAppViewContainer"] {{
    background-color: #09090b;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(0, 191, 255, 0.03), transparent 30%),
        radial-gradient(circle at 90% 80%, rgba(212, 175, 55, 0.04), transparent 30%);
    color: #e4e4e7;
    font-family: 'Inter', sans-serif;
}}

/* Hide standard header */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

/* 3D Floating Interactive Image (OIP.webp) */
.coin-wrapper {{
    position: fixed;
    top: 40px;
    right: 50px;
    width: 130px;
    height: 130px;
    z-index: 999;
    perspective: 1200px;
    animation: floatCoin 5s ease-in-out infinite;
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
        0 10px 30px rgba(0, 0, 0, 0.8),
        0 0 20px rgba(0, 191, 255, 0.15),
        inset 0 0 15px rgba(212, 175, 55, 0.2);
    /* Continuous slow rotation */
    animation: spinCoin 12s linear infinite;
    cursor: pointer;
    transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
}}

/* Interactive reaction on hover - Speeds up, glows cyan/gold */
.coin-3d:hover {{
    animation: spinCoin 2s linear infinite;
    box-shadow: 
        0 0 40px rgba(0, 191, 255, 0.4), 
        0 0 20px rgba(212, 175, 55, 0.4),
        inset 0 0 20px rgba(255, 255, 255, 0.1);
    transform: scale(1.08);
}}

@keyframes spinCoin {{
    0% {{ transform: rotateY(0deg); }}
    100% {{ transform: rotateY(360deg); }}
}}

@keyframes floatCoin {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-15px); }}
}}

/* Typography */
.main-title {{
    color: #ffffff;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 3.5em;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 5px;
    background: linear-gradient(90deg, #ffffff, #a1a1aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.sub-title {{
    color: #71717a;
    text-align: center;
    margin-bottom: 50px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

/* Sleek Block Cards */
.block-card {{
    background: rgba(24, 24, 27, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: all 0.3s ease;
}}

/* Subtle lifting hover effect */
.block-card:hover {{
    transform: translateY(-4px);
    border: 1px solid rgba(212, 175, 55, 0.3);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 191, 255, 0.05);
}}

.block-header {{
    color: #e4e4e7;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 12px;
    margin-bottom: 16px;
    font-family: 'Inter', sans-serif;
    font-size: 1.2em;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

/* Hash Text Styling */
.hash-text {{
    font-family: 'JetBrains Mono', monospace;
    color: #38bdf8;
    word-wrap: break-word;
    font-size: 0.85em;
    background: rgba(0, 0, 0, 0.4);
    padding: 6px 10px;
    border-radius: 6px;
    border-left: 2px solid #38bdf8;
    display: inline-block;
    margin-top: 4px;
    letter-spacing: 0.5px;
}}

/* Streamlit Native Element Overrides */
div.stButton > button {{
    background: #ffffff;
    color: #09090b !important;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1em;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 14px rgba(255, 255, 255, 0.15);
}}

div.stButton > button:hover {{
    background: #e4e4e7;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25);
}}

.stTextArea textarea {{
    background-color: rgba(24, 24, 27, 0.8) !important;
    color: #e4e4e7 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}}

.stTextArea textarea:focus {{
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
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
        # Create Genesis Block if DB is empty
        genesis_block = {
            "index": 0,
            "previous_hash": "0",
            "timestamp": time.time(),
            "data": "Genesis Block - Network Initialized",
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
    
    # Mining (Proof of Work Simulation)
    nonce = 0
    difficulty = 4 # Requires 4 leading zeros
    target = "0" * difficulty
    
    # Minimalist mining progress UI
    mining_placeholder = st.empty()
    
    while True:
        new_hash = hash_block(new_index, previous_hash, timestamp, data, nonce)
        
        if nonce % 10000 == 0:
            mining_placeholder.info(f"⚙️ Computing Hash... Nonce: `{nonce}` | Current: `{new_hash[:12]}...`")
            
        if new_hash.startswith(target):
            mining_placeholder.success(f"✓ Block Validated. Nonce: `{nonce}`")
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
    
    # Save to Supabase
    supabase.table("blocks").insert(new_block).execute()

# --- UI LAYOUT ---
st.markdown('<div class="main-title">HamiZex Core</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Decentralized Cryptographic Ledger Protocol v1.0</div>', unsafe_allow_html=True)

# Transaction Input Form
st.markdown("<h4 style='color: #e4e4e7; font-weight: 600; margin-bottom: 1rem;'>Deploy Transaction</h4>", unsafe_allow_html=True)
with st.container():
    data_input = st.text_area("Enter payload data or contract logic:", height=100, placeholder="{ \"type\": \"transfer\", \"amount\": 0 }")
    if st.button("Sign & Execute Protocol", use_container_width=True):
        if data_input:
            add_block(data_input)
            st.rerun() 
        else:
            st.warning("⚠️ Payload cannot be empty.")

st.markdown("<br><hr style='border: 0; height: 1px; background: rgba(255, 255, 255, 0.05); margin: 2rem 0;'><br>", unsafe_allow_html=True)

# Display the Blockchain
st.markdown("<h4 style='color: #e4e4e7; font-weight: 600; margin-bottom: 1rem;'>Network Ledger</h4>", unsafe_allow_html=True)
blockchain_data = sync_with_supabase()

for block in reversed(blockchain_data):
    st.markdown(f"""
    <div class="block-card">
        <div class="block-header">
            <span>Block #{block['index']}</span>
            <span style="font-size: 0.8em; color: #a1a1aa; font-family: 'JetBrains Mono', monospace;">{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block['timestamp']))}</span>
        </div>
        <div style="margin-bottom: 16px;">
            <span style="color: #a1a1aa; font-size: 0.9em; text-transform: uppercase; font-weight: 600;">Payload Data</span><br>
            <span style="color: #f4f4f5; font-family: 'JetBrains Mono', monospace; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; display: inline-block; width: 100%; margin-top: 4px;">{block['data']}</span>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px;">
            <div>
                <span style="color: #a1a1aa; font-size: 0.8em; text-transform: uppercase; font-weight: 600;">Nonce</span><br>
                <span class="hash-text" style="border-left: 2px solid #a1a1aa; color: #e4e4e7;">{block.get('nonce', 0)}</span>
            </div>
            <div>
                <span style="color: #a1a1aa; font-size: 0.8em; text-transform: uppercase; font-weight: 600;">Previous Hash</span><br>
                <span class="hash-text">{block['previous_hash'][:16]}...{block['previous_hash'][-8:]}</span>
            </div>
        </div>
        
        <div>
            <span style="color: #a1a1aa; font-size: 0.8em; text-transform: uppercase; font-weight: 600;">Block Hash</span><br>
            <span class="hash-text" style="border-left: 2px solid #d4af37; color: #d4af37; font-weight: bold; width: 100%; box-sizing: border-box;">{block['hash']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
