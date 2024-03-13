import streamlit as st
from web3 import Web3
import json
import os
from utils.pinata import upload_file_to_ipfs, upload_json_to_ipfs
from utils.web3_utils import mint_nft

# Load contract ABI and address
with open('src/Marketplace.json', 'r') as file:
    contract_info = json.load(file)
contract_abi = contract_info['abi']
contract_address = contract_info['address']

# Connect to Ethereum network
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Create contract object using web3
nft_marketplace = web3.eth.contract(address=contract_address, abi=contract_abi)

# Page Configurations
st.set_page_config(
    page_title="Apollo NFT Marketplace",
    page_icon="🎨",
    layout="wide"
)

st.title('Apollo NFT Marketplace')

# Connect to MetaMask (you will need to use web3modal or similar in actual production)
st.sidebar.button('Connect Wallet')

# Display NFTs
st.header('NFT Gallery')
if st.sidebar.button('Load NFTs'):
    # Logic to load NFTs goes here
    st.write('NFTs will be displayed here')

# List NFT
st.header('List My NFT')
with st.form('List NFT Form'):
    nft_name = st.text_input('NFT Name')
    nft_description = st.text_area('NFT Description')
    nft_price = st.number_input('Price (in ETH)', min_value=0.01)
    nft_image = st.file_uploader('Upload Image (<500 kB)', type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button('List NFT')
    if submitted and nft_image is not None:
        # Convert the uploaded file to bytes
        image_bytes = nft_image.read()
        # Temporary save image to disk
        temp_file_path = "temp_image.png"
        with open(temp_file_path, "wb") as f:
            f.write(image_bytes)

            # Uploading image to Pinata IPFS
        image_response = upload_file_to_ipfs(temp_file_path)
        if image_response['success']:
            image_ipfs_url = image_response['pinataURL']
            # Cleanup the temporary image file after upload
            os.remove(temp_file_path)
            # Create metadata
            metadata = {
                "name": nft_name,
                "description": nft_description,
                "image": image_ipfs_url
            }
            metadata_response = upload_json_to_ipfs(metadata)
            if metadata_response['success']:
                metadata_ipfs_url = metadata_response['pinataURL']
                seller_private_key = st.text_input('Your Private Key', type='password')  # NEVER expose private keys in production apps
                if seller_private_key:
                    # Attempt to mint NFT with provided metadata URL and price
                    price_wei = web3.to_wei(nft_price, 'ether')
                    tx_receipt = mint_nft(metadata_ipfs_url, price_wei, seller_private_key)
                    if tx_receipt:
                        st.success(f"NFT successfully minted. Transaction hash: {tx_receipt.transactionHash.hex()}")
                    else:
                        st.error("Failed to mint NFT.")
                else:
                    st.warning("Enter your private key to mint the NFT.")
                st.success(f'NFT successfully listed with IPFS URL: {metadata_ipfs_url}')
            else:
                st.error("Failed to upload NFT metadata to IPFS.")
        else:
            st.error("Failed to upload image to IPFS.")
    elif submitted:
        st.error("Please upload an image for the NFT.")

# Auctions (this will need more logic to handle auctions based on your contract)
st.header('Auctions')
# Logic to handle and display auctions

# additional functionality needed:
# - Interacting with MetaMask to handle transactions
# - Uploading images to IPFS and storing the metadata
# - Real-time updating of NFT listings and auctions