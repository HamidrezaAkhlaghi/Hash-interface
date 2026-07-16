import streamlit as st
import hashlib
import time
from supabase import create_client, Client

# --- Page Config ---
st.set_page_config(page_title="HamiZex Blockchain", page_icon="🪙", layout="wide")

# --- Custom CSS for Sexy UI & Rotating Coin ---
st.markdown("""
<style>
    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #131417, #1e2128, #2a2d35);
        color: white;
    }
    
    /* Neon headers */
    h1, h2, h3 {
        color: #00ffcc !important; /* Cyberpunk Cyan */
        text-shadow: 0px 0px 15px rgba(0, 255, 204, 0.4);
    }

    /* Styled metric boxes */
    div[data-testid="stMetricValue"] {
        color: #f7931a !important; /* Bitcoin Orange accent */
    }
    
    /* Rotating Coin Animation */
    .rotating-coin {
        width: 120px;
        height: 120px;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg');
        background-size: cover;
        margin: 0 auto;
        animation: spin 5s linear infinite;
        transition: transform 0.4s ease-out;
        filter: drop-shadow(0 0 15px rgba(247, 147, 26, 0.5));
    }
    
    /* Speed up spin on hover (Mouse interaction) */
    .rotating-coin:hover {
        animation: spin 0.4s linear infinite;
        transform: scale(1.3);
        filter: drop-shadow(0 0 25px rgba(247, 147, 26, 0.9));
        cursor: pointer;
    }

    @keyframes spin { 
        100% { -webkit-transform: rotateY(360deg); transform: rotateY(360deg); } 
    }
    
    /* Style the block cards */
    .block-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #00ffcc;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.2s;
    }
    
    .block-card:hover {
        transform: translateX(10px);
        background: rgba(255, 255, 255, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# --- Supabase Setup ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Fetch Blocks ---
def get_blocks():
    response = supabase.table("blocks").select("*").order("index", desc=False).execute()
    return response.data

# --- Add Block ---
def add_block(data):
    chain = get_blocks()
    if len(chain) == 0:
        index = 0
        previous_hash = "0"
    else:
        last_block = chain[-1]
        index = last_block['index'] + 1
        previous_hash = last_block['hash']
        
    timestamp = str(time.time())
    
    # Proof of Work (Mining) - Simple Version
    nonce = 0
    with st.spinner("⚡ Processing HamiZex Transaction..."):
        while True:
            hash_string = str(index) + timestamp + data + previous_hash + str(nonce)
            block_hash = hashlib.sha256(hash_string.encode()).hexdigest()
            if block_hash.startswith("0000"):  # Difficulty
                break
            nonce += 1
            
    new_block = {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
        "hash": block_hash,
        "nonce": nonce
    }
    
    supabase.table("blocks").insert(new_block).execute()
    return new_block

# --- UI Layout ---
st.write("") # Spacer
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div class="rotating-coin"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; margin-top: 20px;'>HamiZex ($HZX)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b9bb4; font-size: 18px;'>The Decentralized Ledger by Hamidreza & Hami</p>", unsafe_allow_html=True)

# Main Interface
st.write("---")

col_data, col_chain = st.columns([1, 2])

with col_data:
    st.subheader("Initiate Transaction")
    data_input = st.text_area("Enter transaction details or smart contract message:", height=100)
    
    if st.button("Cryptographically Sign & Mine ⛏️", use_container_width=True):
        if data_input:
            add_block(data_input)
            st.success(f"Transaction verified and added to HamiZex!")
            st.rerun()
        else:
            st.warning("Data payload cannot be empty.")
            
    st.write("")
    st.metric(label="Network Difficulty Target", value="4 Leading Zeros")
    st.metric(label="Consensus Protocol", value="Proof-of-Work (PoW)")
    
with col_chain:
    st.subheader("Live Network Ledger")
    blocks = get_blocks()
    
    if len(blocks) == 0:
        st.info("The HamiZex ledger is currently empty. Initialize the genesis block!")
    else:
        # Display blocks beautifully using HTML
        for block in reversed(blocks): # Show newest first
            st.markdown(f"""
            <div class="block-card">
                <h4 style="color: white; margin-bottom: 5px;">📦 Block #{block['index']}</h4>
                <p style="color: #00ffcc; font-size: 15px;"><b>Payload:</b> {block['data']}</p>
                <div style="font-family: monospace; font-size: 13px; color: #8b9bb4; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px;">
                    <div><b style="color: #f7931a;">Hash:</b> {block['hash']}</div>
                    <div style="margin-top: 4px;"><b>Prev:</b> {block['previous_hash']}</div>
                    <div style="margin-top: 4px;"><b>Nonce:</b> {block['nonce']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
