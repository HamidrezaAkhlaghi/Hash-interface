import streamlit as st
import streamlit.components.v1 as components
import hashlib
import base64
import time
import os

# ==========================================================
#  ⚙️ LOGIC — (your technical stuff, unchanged)
# ==========================================================
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev = self.get_latest_block()
        new_block = Block(prev.index + 1, time.time(), data, prev.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i - 1]
            if cur.hash != cur.calculate_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
        return True

# ==========================================================
#  🎨 UI — SEXY MODE
# ==========================================================
st.set_page_config(page_title="₿ MY BLOCKCHAIN", page_icon="🪙", layout="wide")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

coin_b64 = get_image_base64("OIP.webp")   # <-- your image

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* ============ CINEMATIC BACKGROUND (OIP.webp) ============ */
[data-testid="stAppViewContainer"] {{
    background-color: #060a14;
    background-image:
        radial-gradient(ellipse at center, rgba(6,10,20,0.40) 0%, rgba(6,10,20,0.93) 80%),
        radial-gradient(circle at 78% 22%, rgba(212,160,60,0.10), transparent 45%),
        radial-gradient(circle at 18% 82%, rgba(60,110,220,0.09), transparent 50%),
        url('data:image/webp;base64,{coin_b64}');
    background-size: cover, cover, cover, cover;
    background-position: center;
    background-attachment: fixed;
    color: #e4e4e7;
    font-family: 'Inter', sans-serif;
}}

/* golden particle drift */
[data-testid="stAppViewContainer"]::before {{
    content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
        radial-gradient(2px 2px at 20% 30%, rgba(253,224,71,0.55), transparent),
        radial-gradient(1.5px 1.5px at 70% 60%, rgba(212,175,55,0.45), transparent),
        radial-gradient(2px 2px at 45% 85%, rgba(120,170,255,0.35), transparent),
        radial-gradient(1px 1px at 85% 15%, rgba(253,224,71,0.5), transparent);
    background-size: 200% 200%;
    animation: drift 22s linear infinite;
}}
@keyframes drift {{ 0% {{background-position: 0% 0%;}} 100% {{background-position: 200% 200%;}} }}

[data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}

/* ============ FLOATING 3D COIN (mouse parallax via JS) ============ */
.coin-wrapper {{
    position: fixed; top: 45px; right: 55px;
    width: 150px; height: 150px; z-index: 999;
    perspective: 1200px;
    animation: floatCoin 4s ease-in-out infinite;
    filter: drop-shadow(0 0 35px rgba(212,175,55,0.35));
    transition: transform 0.15s ease-out;
}}
.coin-3d {{
    width: 100%; height: 100%; border-radius: 50%;
    background-image: url('data:image/webp;base64,{coin_b64}');
    background-size: cover; background-position: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.9), 0 0 30px rgba(212,175,55,0.35),
                inset 0 0 25px rgba(255,215,120,0.15);
    animation: spinCoin 15s linear infinite;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.25,0.8,0.25,1);
}}
.coin-3d:hover {{
    animation: spinCoin 1.2s linear infinite;
    box-shadow: 0 0 70px rgba(253,224,71,0.7), inset 0 0 35px rgba(255,255,255,0.25);
    transform: scale(1.12);
}}
@keyframes spinCoin  {{ 0% {{transform: rotateY(0);}} 100% {{transform: rotateY(360deg);}} }}
@keyframes floatCoin {{ 0%,100% {{transform: translateY(0);}} 50% {{transform: translateY(-14px);}} }}

/* ============ MOUSE-DRIVEN GEARS ============ */
.gear {{
    position: fixed; z-index: 0; pointer-events: none;
    color: rgba(212,175,55,0.30);
    text-shadow: 0 0 25px rgba(212,175,55,0.35);
    transition: transform 0.1s linear;
    user-select: none;
}}
#gear1 {{ top: 12%;  left: 3%;  font-size: 130px; }}
#gear2 {{ top: 55%;  left: 8%;  font-size: 75px; color: rgba(120,170,255,0.25); }}
#gear3 {{ bottom: 8%; right: 6%; font-size: 100px; }}
#gear4 {{ top: 30%;  right: 18%; font-size: 55px; color: rgba(253,224,71,0.22); }}

/* ============ TYPOGRAPHY ============ */
.main-title {{
    text-align: center; font-size: 4.2em; font-weight: 800; letter-spacing: -1px;
    margin-bottom: 5px;
    background: linear-gradient(90deg, #b8860b, #fde047, #ffffff, #fde047, #b8860b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-size: 300% auto;
    animation: shimmer 4s infinite linear;
}}
@keyframes shimmer {{ to {{ background-position: 300% center; }} }}
.sub-title {{
    color: #8b9cc4; text-align: center; margin-bottom: 45px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1em; letter-spacing: 3px; text-transform: uppercase;
}}

/* ============ GLASS BLOCK CARDS ============ */
.block-card {{
    position: relative;
    background: linear-gradient(160deg, rgba(13,20,38,0.72), rgba(8,12,24,0.85));
    border: 1px solid rgba(212
