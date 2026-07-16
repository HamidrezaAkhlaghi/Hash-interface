import streamlit as st
import hashlib
import time

# ==========================================
# 1. BLOCK AND BLOCKCHAIN ENGINE
# ==========================================

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Manually construct the first block (index 0)
        timestamp = time.time()
        genesis_hash = self.calculate_hash(0, "0", timestamp, "Genesis Block")
        genesis_block = Block(0, "0", timestamp, "Genesis Block", genesis_hash)
        self.chain.append(genesis_block)

    def calculate_hash(self, index, previous_hash, timestamp, data):
        # Creates a SHA-256 hash based on the block's details
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        index = latest_block.index + 1
        timestamp = time.time()
        previous_hash = latest_block.hash
        new_hash = self.calculate_hash(index, previous_hash, timestamp, data)
        
        new_block = Block(index, previous_hash, timestamp, data, new_hash)
        self.chain.append(new_block)

# ==========================================
# 2. STREAMLIT WEB INTERFACE
# ==========================================

# Initialize the blockchain in Streamlit's session state 
# (This keeps the chain from resetting every time you click a button)
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# App layout and text
st.title("My Collaborative Blockchain")
st.write("Add data to the chain and see the cryptographic hashes update in real time!")

# Input area for users to type data
new_data = st.text_input("Enter data for the new block:")

# The button to trigger adding a new block
if st.button("Add Block"):
    if new_data:
        st.session_state.blockchain.add_block(new_data)
        st.success(f"Block added successfully with data: {new_data}")
    else:
        st.warning("Please enter some data before adding a block.")

# Displaying the blockchain visually
st.subheader("Current Blockchain Ledger:")

# Loop through the chain and create a dropdown box for each block
for block in st.session_state.blockchain.chain:
    with st.expander(f"Block {block.index}: {block.data}"):
        st.write(f"**Index:** {block.index}")
        st.write(f"**Timestamp:** {block.timestamp}")
        st.write(f"**Data:** {block.data}")
        st.write(f"**Previous Hash:** `{block.previous_hash}`")
        st.write(f"**Hash:** `{block.hash}`")
