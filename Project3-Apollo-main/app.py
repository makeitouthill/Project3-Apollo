import streamlit as st
from web3 import Web3
import json

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
    # Fetch the total number of NFTs from the contract
    total_nfts = nft_marketplace.functions.totalSupply().call()
    st.write(f'Total NFTs: {total_nfts}')

    # Loop through each NFT and display its details
    for nft_id in range(total_nfts):
        # Fetch NFT details from the contract
        nft_details = nft_marketplace.functions.tokenDetails(nft_id).call()
        nft_name, nft_description, nft_price, nft_image_uri = nft_details

        # Display NFT details
        st.write(f'NFT ID: {nft_id}')
        st.image(nft_image_uri, caption=nft_name, width=200)
        st.write(f'Description: {nft_description}')
        st.write(f'Price: {web3.fromWei(nft_price, "ether")} ETH')

# List NFT
st.header('List My NFT')
with st.form('List NFT Form'):
    nft_name = st.text_input('NFT Name')
    nft_description = st.text_area('NFT Description')
    nft_price = st.number_input('Price (in ETH)', min_value=0.01)
    # Upload image will require handling image uploads, storing to IPFS, and getting the URI
    nft_image = st.file_uploader('Upload Image (<200 kB)', type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button('List NFT')
    if submitted:
        st.write(f'You are listing {nft_name} for {nft_price} ETH')

# Auctions (this will need more logic to handle auctions based on your contract)
st.header('Auctions')
# Logic to handle and display auctions