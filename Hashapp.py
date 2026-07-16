import streamlit as st
import hashlib
import time
import base64
import os
from supabase import create_client, Client

# --- SETUP & CONFIG ---
st.set_page_config(page_title="Dr. Fluffy's ABDI Coin Emporium", page_icon="😸", layout="centered")

# --- IMAGE ENCODING FOR UI ---
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Read the local image file verbatim
coin_b64 = get_image_base64("OIP_2.webp")

# --- HUMOROUS CSS UI DESIGN ---
page_bg_img = f"""
<style>
/* Import web fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Comic+Neue:wght@700&display=swap');

/* Main Background */
[data-testid="stAppViewContainer"] {{
    background-color: #000000;
    background-image: 
        linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)),
        url('data:image/webp;base64,{coin_b64}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}}

/* Hide standard header */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

/* Centered Joke Container */
.fluffy-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 5vh;
    padding: 40px;
    background: rgba(0, 0, 0, 0.5);
    border: 2px dashed rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    backdrop-filter: blur(5px);
}}

.title-text {{
    font-family: 'Inter', sans-serif;
    font-size: 2.5em;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
}}

.body-text {{
    font-family: 'Inter', sans-serif;
    font-size: 1.2em;
    line-height: 1.6;
    margin-bottom: 20px;
    max-width: 600px;
}}

.ufo-cat {{
    font-size: 4em;
    margin: 20px 0;
    animation: floatCat 3s ease-in-out infinite;
}}

@keyframes floatCat {{
    0%, 100% {{ transform: translateY(0px) rotate(-5deg); }}
    50% {{ transform: translateY(-15px) rotate(5deg); }}
}}

.footer-text {{
    font-size: 0.8em;
    color: #a1a1aa;
    margin-top: 40px;
    font-family: 'Comic Neue', cursive;
}}

/* Streamlit Button Override (DONATE LINT & REGRET IT) */
div.stButton > button {{
    background-color: #ffffff !important;
    color: #000000 !important;
    font-family: 'Inter', sans-serif;
    font-weight: 900;
    font-size: 1.2em;
    border: 2px solid #000000;
    border-radius: 5px;
    padding: 15px 30px;
    text-transform: uppercase;
    transition: all 0.2s ease;
    box-shadow: 5px 5px 0px rgba(255,255,255,0.3);
}}

div.stButton > button:hover {{
    transform: translate(2px, 2px);
    box-shadow: 3px 3px 0px rgba(255,255,255,0.3);
    background-color: #f0f0f0 !important;
}}

/* Block styling */
.block-card {{
    background: rgba(20, 20, 20, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 15px;
    text-align: left;
    font-family: monospace;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- INITIALIZE FUNNY TOAST ---
if "toast_shown" not in st.session_state:
    st.toast("🫖 **Error 418: I'm a teapot**, and this background is too serious for this webpage content.", icon="⚠️")
    st.session_state.toast_shown = True

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
            "data": "Genesis Block - Dr. Fluffy Initialized ABDI Coin",
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
    difficulty = 3 # Lowered slightly so you don't wait forever while laughing
    target = "0" * difficulty
    
    mining_placeholder = st.empty()
    
    while True:
        new_hash = hash_block(new_index, previous_hash, timestamp, data, nonce)
        
        if nonce % 5000 == 0:
            mining_placeholder.info(f"🛸 Abducting hashes... Nonce: `{nonce}`")
            
        if new_hash.startswith(target):
            mining_placeholder.success(f"😸 Success! ABDI Block Mined. Nonce: `{nonce}`")
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
st.markdown("""
<div class="fluffy-container">
    <div class="title-text">DR. FLUFFY'S GALACTIC ABDI COIN EMPORIUM</div>
    <div class="ufo-cat">🛸😸</div>
    <div class="body-text">
        Welcome to our page. I thought the background source code was in a repo named <b>"serious_crypto_v4"</b> 
        but it was actually in <b>"broken_lint_collect_v1"</b>.<br><br>
        Our frontend dev is still learning CSS.
    </div>
    <div class="body-text" style="font-weight: bold;">
        Current Inventory: zero toe lint.<br>
        But we have ABDI COIN and this BACKGROUND.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # Spacer

# Transaction Input Form
data_input = st.text_input("Enter ABDI Transaction Data:", placeholder="I traded 5 toe lints for 1 ABDI Coin...")
if st.button("DONATE LINT & REGRET IT.", use_container_width=True):
    if data_input:
        add_block(data_input)
        st.toast("Block successfully deployed to the lint network!", icon="🚀")
        time.sleep(1)
        st.rerun() 
    else:
        st.warning("⚠️ You must enter some data before regretting it.")

st.divider()

# Display the Blockchain
st.markdown("<h3 style='text-align: center;'>ABDI Network Ledger</h3>", unsafe_allow_html=True)
blockchain_data = sync_with_supabase()

for block in reversed(blockchain_data):
    st.markdown(f"""
    <div class="block-card">
        <b style="color:#fde047;">Block #{block['index']}</b> | <i>{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block['timestamp']))}</i><br><br>
        <b>Payload:</b> {block['data']}<br><br>
        <b>Nonce:</b> {block.get('nonce', 0)}<br>
        <b>Prev Hash:</b> {block['previous_hash']}<br>
        <b style="color:#38bdf8;">Hash:</b> {block['hash']}
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer-text' style='text-align: center;'>© 2026 Toe-Lint Corp. Built on hope and a broken npm install.</div>", unsafe_allow_html=True)
