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

# Read the local image file verbatim
coin_b64 = get_image_base64("OIP_2.webp")

# --- MINIMALIST & BEAUTIFUL CSS ---
page_bg_img = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&family=Fira+Code:wght@400;500&display=swap');

/* Clean, dark background with subtle image integration */
[data-testid="stAppViewContainer"] {{
    background-color: #050505;
    background-image: 
        linear-gradient(rgba(5, 5, 5, 0.85), rgba(5, 5, 5, 0.95)),
        url('data:image/webp;base64,{coin_b64}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ededed;
    font-family: 'Inter', sans-serif;
}}

/* Hide standard header for a cleaner look */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

/* Elegant Typography */
.main-title {{
    font-family: 'Inter', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #ffffff;
    text-align: center;
    margin-bottom: 0.2rem;
}}

.sub-title {{
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: #a1a1aa;
    text-align: center;
    margin-bottom: 3rem;
    letter-spacing: 0.5px;
}}

/* Sleek Glass Cards */
.glass-card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.2s ease, border-color 0.2s ease;
}}

.glass-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(212, 175, 55, 0.3);
}}

/* Ledger specific styles */
.block-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 12px;
    margin-bottom: 16px;
}}

.block-id {{
    font-size: 1.1rem;
    font-weight: 500;
    color: #d4af37;
}}

.block-time {{
    font-size: 0.85rem;
    color: #71717a;
}}

.data-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #71717a;
    margin-bottom: 4px;
    display: block;
}}

.mono-text {{
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    color: #d4d4d8;
    word-break: break-all;
}}

/* Input Area Restyling */
.stTextArea textarea {{
    background-color: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #ededed !important;
    font-family: 'Fira Code', monospace !important;
    border-radius: 12px !important;
    padding: 16px !important;
}}

.stTextArea textarea:focus {{
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 1px #d4af37 !important;
}}

/* Button Restyling */
div.stButton > button {{
    background-color: #ffffff;
    color: #000000 !important;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    border-radius: 12px;
    border: none;
    padding: 12px 24px;
    transition: all 0.2s ease;
}}

div.stButton > button:hover {{
    background-color: #d4af37;
    color: #ffffff !important;
    transform: scale(1.01);
}}
</style>
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
            mining_placeholder.info(f"Computing Hash... Nonce: {nonce}")
            
        if new_hash.startswith(target):
            mining_placeholder.success("Block successfully verified and appended.")
            time.sleep(1) # Brief pause so the user sees the success message
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
st.markdown('<div class="sub-title">A Secure, Minimalist Decentralized Ledger</div>', unsafe_allow_html=True)

# Transaction Entry
with st.container():
    st.markdown('<span class="data-label">New Transaction Payload</span>', unsafe_allow_html=True)
    data_input = st.text_area("Payload", height=100, label_visibility="collapsed", placeholder="Enter smart contract data or transfer details...")
    
    if st.button("Sign & Append Block", use_container_width=True):
        if data_input.strip():
            add_block(data_input)
            st.rerun() 
        else:
            st.warning("Payload cannot be empty.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<span class="data-label" style="font-size: 0.9rem;">Network Ledger History</span>', unsafe_allow_html=True)

# Ledger Rendering
blockchain_data = sync_with_supabase()

for block in reversed(blockchain_data):
    st.markdown(f"""
    <div class="glass-card">
        <div class="block-header">
            <span class="block-id">Block {block['index']}</span>
            <span class="block-time">{time.strftime('%b %d, %Y • %H:%M:%S', time.localtime(block['timestamp']))}</span>
        </div>
        
        <div style="margin-bottom: 16px;">
            <span class="data-label">Payload</span>
            <span class="mono-text" style="color: #ffffff;">{block['data']}</span>
        </div>
        
        <div style="display: flex; gap: 40px; margin-bottom: 16px;">
            <div>
                <span class="data-label">Nonce</span>
                <span class="mono-text">{block.get('nonce', 0)}</span>
            </div>
            <div style="flex-grow: 1;">
                <span class="data-label">Previous Hash</span>
                <span class="mono-text">{block['previous_hash']}</span>
            </div>
        </div>
        
        <div>
            <span class="data-label">Block Hash</span>
            <span class="mono-text" style="color: #d4af37;">{block['hash']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
