import streamlit as st
import hashlib
import time
from supabase import create_client, Client

# --- SETUP & CONFIG ---
st.set_page_config(page_title="HamiZex Blockchain", page_icon="🪙", layout="wide")

# --- CSS UI DESIGN (Bitcoin & Trading Vibe) ---
page_bg_img = """
<style>
/* Background Image of Bitcoin & Trading Charts */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1621416894569-0f39ed31d247?auto=format&fit=crop&q=80&w=2000");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Make header transparent so it doesn't block the background */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Main Title Styling */
.main-title {
    color: #FFD700; /* Gold */
    text-align: center;
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 215, 0, 0.4);
    font-family: 'Courier New', Courier, monospace;
    font-size: 3.5em;
    font-weight: 800;
    margin-bottom: 5px;
}

.sub-title {
    color: #F0F0F0;
    text-align: center;
    margin-bottom: 40px;
    font-size: 1.2em;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.8);
}

/* Glassmorphism Block Cards with Gold Borders */
.block-card {
    background: rgba(18, 18, 22, 0.85);
    border: 1px solid #FFD700;
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 8px 32px rgba(255, 215, 0, 0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    color: #E0E0E0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.block-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(255, 215, 0, 0.3);
}

.block-header {
    color: #FFD700;
    border-bottom: 1px solid rgba(255, 215, 0, 0.3);
    padding-bottom: 10px;
    margin-bottom: 15px;
    font-size: 1.5em;
    font-weight: bold;
}

/* Hash Text Styling */
.hash-text {
    font-family: 'Courier New', Courier, monospace;
    color: #00FFCC; /* Neon cyan for cryptographic hashes */
    word-wrap: break-word;
    background: rgba(0, 0, 0, 0.5);
    padding: 2px 6px;
    border-radius: 4px;
}
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
            mining_placeholder.info(f"⛏️ Mining... Trying nonce: {nonce} | Hash: {new_hash[:15]}...")
            
        if new_hash.startswith(target):
            mining_placeholder.success(f"💎 Block Mined Successfully! Nonce found: {nonce}")
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
st.markdown('<div class="main-title">🪙 HamiZex Blockchain</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A Secure, Decentralized Ledger by Hamidreza ($HZX)</div>', unsafe_allow_html=True)

# Transaction Input Form
st.markdown("### 📝 Initiate Transaction")
with st.container():
    data_input = st.text_area("Enter transaction details or smart contract message:", height=100)
    if st.button("Cryptographically Sign & Mine ⛏️", use_container_width=True):
        if data_input:
            add_block(data_input)
            st.rerun() # Refresh the app to show the new block
        else:
            st.warning("⚠️ Transaction data cannot be empty.")

st.divider()

# Display the Blockchain
st.markdown("### ⛓️ Live Public Ledger")
blockchain_data = sync_with_supabase()

for block in reversed(blockchain_data):
    st.markdown(f"""
    <div class="block-card">
        <div class="block-header">Block #{block['index']}</div>
        <b>Timestamp:</b> {time.ctime(block['timestamp'])}<br><br>
        <b>Transaction Data:</b><br>
        <i>{block['data']}</i><br><br>
        <b>Nonce:</b> <span class="hash-text">{block.get('nonce', 0)}</span><br>
        <b>Previous Hash:</b> <br><span class="hash-text">{block['previous_hash']}</span><br>
        <b>Block Hash:</b> <br><span class="hash-text">{block['hash']}</span>
    </div>
    """, unsafe_allow_html=True)
