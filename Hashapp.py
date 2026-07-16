import streamlit as st
import hashlib
import time
from supabase import create_client, Client

# --- SETUP & CONFIG ---
st.set_page_config(page_title="HamiZex Blockchain", page_icon="🪙", layout="wide")

# --- PREMIUM CSS UI DESIGN (Cyberpunk / Gold Crypto Vibe) ---
page_bg_img = """
<style>
/* Import futuristic fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');

/* Dynamic Background */
[data-testid="stAppViewContainer"] {
    background-color: #0b0c10;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(255, 215, 0, 0.08), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(0, 255, 204, 0.05), transparent 25%),
        url("https://www.transparenttextures.com/patterns/cubes.png");
    background-attachment: fixed;
}

/* Hide standard header */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* 3D Floating Interactive Coin */
.coin-wrapper {
    position: fixed;
    top: 30px;
    right: 50px;
    width: 80px;
    height: 80px;
    z-index: 999;
    perspective: 1000px;
}

.coin-3d {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #FFDF00, #DAA520, #8B6508);
    box-shadow: 
        0 0 20px rgba(255, 215, 0, 0.6),
        inset 0 0 15px rgba(255,255,255,0.8),
        inset 0 0 30px rgba(218, 165, 32, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 35px;
    color: #fff;
    text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
    border: 2px solid #FFF380;
    /* Continuous rotation + floating */
    animation: spinCoin 4s linear infinite, floatCoin 3s ease-in-out infinite;
    cursor: crosshair;
    transition: all 0.3s ease;
}

/* Interactive reaction on hover */
.coin-3d:hover {
    animation: spinCoin 0.5s linear infinite; /* Speeds up on mouse hover */
    box-shadow: 0 0 50px rgba(255, 215, 0, 1), inset 0 0 20px rgba(255,255,255,1);
    transform: scale(1.1);
}

@keyframes spinCoin {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}

@keyframes floatCoin {
    0%, 100% { margin-top: 0px; }
    50% { margin-top: -15px; }
}

/* Titles */
.main-title {
    color: #FFD700;
    text-align: center;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.5), 0 0 20px rgba(255, 215, 0, 0.3);
    font-family: 'Orbitron', sans-serif;
    font-size: 4em;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: -10px;
    animation: pulseGlow 2s ease-in-out infinite alternate;
}

@keyframes pulseGlow {
    from { text-shadow: 0 0 10px #FFD700, 0 0 20px #FFD700; }
    to { text-shadow: 0 0 20px #FFD700, 0 0 30px #FF8C00; }
}

.sub-title {
    color: #c5c6c7;
    text-align: center;
    margin-bottom: 50px;
    font-family: 'Space Mono', monospace;
    font-size: 1.2em;
    letter-spacing: 1px;
}

/* Glassmorphism Block Cards with 3D Mouse Tilt effect */
.block-card {
    background: linear-gradient(135deg, rgba(31, 33, 40, 0.8) 0%, rgba(18, 18, 22, 0.9) 100%);
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    color: #E0E0E0;
    font-family: 'Space Mono', monospace;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Sexy Hover Effect: Tilts toward the mouse */
.block-card:hover {
    transform: translateY(-8px) scale(1.02);
    border: 1px solid rgba(255, 215, 0, 0.8);
    box-shadow: 0 15px 40px rgba(255, 215, 0, 0.2), inset 0 0 15px rgba(255, 215, 0, 0.05);
}

.block-header {
    color: #FFD700;
    border-bottom: 2px dashed rgba(255, 215, 0, 0.2);
    padding-bottom: 15px;
    margin-bottom: 20px;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.8em;
    font-weight: 700;
    text-transform: uppercase;
}

/* Hash Text Styling */
.hash-text {
    font-family: 'Space Mono', monospace;
    color: #66fcf1;
    word-wrap: break-word;
    background: rgba(0, 0, 0, 0.6);
    padding: 4px 8px;
    border-radius: 6px;
    border-left: 3px solid #66fcf1;
    display: inline-block;
    margin-top: 5px;
}

/* Streamlit Native Element Styling (Buttons & Text Area) */
div.stButton > button {
    background: linear-gradient(90deg, #D4AF37 0%, #FFD700 50%, #D4AF37 100%);
    background-size: 200% auto;
    color: #121212 !important;
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    transition: 0.5s;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

div.stButton > button:hover {
    background-position: right center;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.8);
    transform: scale(1.02);
}

.stTextArea textarea {
    background-color: rgba(0, 0, 0, 0.5) !important;
    color: #66fcf1 !important;
    font-family: 'Space Mono', monospace !important;
    border: 1px solid rgba(255, 215, 0, 0.3) !important;
    border-radius: 8px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #FFD700 !important;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.3) !important;
}
</style>

<!-- Floating 3D Coin HTML Component -->
<div class="coin-wrapper">
    <div class="coin-3d">Z</div>
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
            "data": "Genesis Block - Welcome to HamiZex",
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
    
    # UI Element to show mining progress
    mining_placeholder = st.empty()
    
    while True:
        new_hash = hash_block(new_index, previous_hash, timestamp, data, nonce)
        
        if nonce % 10000 == 0: # Update UI occasionally to avoid freezing
            mining_placeholder.info(f"⛏️ **Mining Protocol Active...** Trying nonce: `{nonce}` | Hash: `{new_hash[:15]}...`")
            
        if new_hash.startswith(target):
            mining_placeholder.success(f"💎 **Block Mined Successfully!** Nonce found: `{nonce}`")
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
st.markdown('<div class="main-title">HamiZex Network</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Decentralized Cryptographic Ledger • Native Token ($HZX)</div>', unsafe_allow_html=True)

# Transaction Input Form
st.markdown("<h3 style='color: #FFD700; font-family: Orbitron;'>📝 INITIATE TRANSACTION</h3>", unsafe_allow_html=True)
with st.container():
    data_input = st.text_area("Enter transaction payload or smart contract hex:", height=120)
    if st.button("Cryptographically Sign & Mine Block ⛏️", use_container_width=True):
        if data_input:
            add_block(data_input)
            st.rerun() # Refresh the app to show the new block
        else:
            st.warning("⚠️ Transaction payload cannot be empty.")

st.markdown("<br><hr style='border: 1px solid rgba(0, 255, 204, 0.3);'><br>", unsafe_allow_html=True)

# Display the Blockchain
st.markdown("<h3 style='color: #FFD700; font-family: Orbitron;'>⛓️ LIVE PUBLIC LEDGER</h3>", unsafe_allow_html=True)
blockchain_data = sync_with_supabase()

for block in reversed(blockchain_data):
    st.markdown(f"""
    <div class="block-card">
        <div class="block-header">Block #{block['index']}</div>
        <b>Timestamp:</b> <span style="color:#66fcf1;">{time.ctime(block['timestamp'])}</span><br><br>
        <b>Transaction Data:</b><br>
        <span style="color:#e0e0e0; font-style: italic;">{block['data']}</span><br><br>
        <b>Nonce:</b> <br><span class="hash-text">{block.get('nonce', 0)}</span><br><br>
        <b>Previous Hash:</b> <br><span class="hash-text">{block['previous_hash']}</span><br><br>
        <b>Block Hash:</b> <br><span class="hash-text">{block['hash']}</span>
    </div>
    """, unsafe_allow_html=True)
