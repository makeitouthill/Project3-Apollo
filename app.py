import streamlit as st
from web3 import Web3
import json
import os
from utils.pinata import upload_file_to_ipfs, upload_json_to_ipfs
from utils.web3_utils import mint_nft
import requests

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

# Connect to MetaMask
st.sidebar.button('Connect Wallet')

# Display NFTs
st.header('NFT Gallery')
if st.sidebar.button('Load NFTs'):
    try:
        total_nfts = nft_marketplace.functions.totalSupply().call()
        for i in range(total_nfts):
            token_id = i + 1
            metadata_uri = nft_marketplace.functions.tokenURI(token_id).call()
            response = requests.get(metadata_uri)
            if response.status_code == 200:
                metadata = response.json()
                # Fallbacks for name and description if they're not provided in the metadata
                nft_name = metadata.get("name", f"N/A (Token ID: {token_id})")
                nft_description = metadata.get("description", "No description available.")
                image_url = metadata.get("image", "")
                
                # Ensure there's an image URL to attempt loading
                if image_url:
                    st.image(image_url, width=200)
                    st.write(f'Name: {nft_name}')
                    st.write(f'Description: {nft_description}')
                    st.write(f'Token ID: {token_id}')
                else:
                    st.error(f'No image URL for Token ID: {token_id}')
            else:
                st.error(f'Failed to load metadata for Token ID: {token_id}')
    except Exception as e:
        st.error(f'Error loading NFTs: {str(e)}')

# List NFT
st.header('List My NFT')
with st.form('List NFT Form', clear_on_submit=True):
    nft_name = st.text_input('NFT Name')
    nft_description = st.text_area('NFT Description')
    nft_price = st.number_input('Price (in ETH)', min_value=0.01)
    nft_image = st.file_uploader('Upload Image (<500 kB)', type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button('List NFT')

if submitted:
    if nft_image is not None:
        # Upload image to IPFS and get the URI
        image_uri_response = upload_file_to_ipfs(nft_image)
        if image_uri_response and image_uri_response.get('success'):
            image_ipfs_url = image_uri_response.get('pinataURL')

            # Preparing Metadata
            nft_metadata = {
                "name": nft_name,
                "description": nft_description,
                "image": image_ipfs_url,
                "attributes": [{"trait_type": "Price", "value": f"{nft_price} ETH"}]
            }
            # Upload Metadata to IPFS
            metadata_uri_response = upload_json_to_ipfs(nft_metadata)
            if metadata_uri_response and metadata_uri_response.get('success'):
                metadata_ipfs_url = metadata_uri_response.get('pinataURL')
                
                # Mint NFT with metadata
                price_wei = web3.toWei(nft_price, 'ether')
                try:
                    tx_hash = nft_marketplace.functions.createToken(metadata_ipfs_url, price_wei).transact({'from': web3.eth.accounts[0], 'value': web3.toWei(0.01, 'ether')})
                    st.success(f'NFT successfully minted with metadata. Transaction Hash: {tx_hash.hex()}')
                except Exception as e:
                    st.error(f'Error minting NFT: {e}')
            else:
                st.error('Failed to upload NFT metadata to IPFS.')
        else:
            st.error('Failed to upload image to IPFS.')
    else:
        st.error('Please upload an image for the NFT.')

# Auctions
st.header('Auctions')
with st.form('Create Auction Form'):
    auction_token_id = st.number_input('Token ID', min_value=1)
    auction_min_price = st.number_input('Minimum Price (in ETH)', min_value=0.01)
    auction_duration = st.number_input('Duration (in seconds)', min_value=60)
    create_auction = st.form_submit_button('Create Auction')
    if create_auction:
        account = web3.eth.accounts[0]
        tx_hash = nft_marketplace.functions.createAuction(auction_token_id, web3.toWei(auction_min_price, 'ether'), auction_duration).transact({'from': account})
        st.write(f'Auction created for Token ID {auction_token_id}. Transaction Hash: {tx_hash.hex()}')

st.header('Bid on Auctions')
with st.form('Bid Form'):
    bid_token_id = st.number_input('Token ID to Bid On', min_value=1)
    bid_amount = st.number_input('Bid Amount (in ETH)', min_value=0.01)
    place_bid = st.form_submit_button('Place Bid')
    if place_bid:
        account = web3.eth.accounts[0]
        tx_hash = nft_marketplace.functions.bid(bid_token_id).transact({'from': account, 'value': web3.toWei(bid_amount, 'ether')})
        st.write(f'Bid placed for Token ID {bid_token_id} with amount {bid_amount} ETH. Transaction Hash: {tx_hash.hex()}')

st.header('End Auctions')
with st.form('End Auction Form'):
    end_auction_token_id = st.number_input('Token ID to End Auction', min_value=1)
    end_auction = st.form_submit_button('End Auction')
    if end_auction:
        account = web3.eth.accounts[0]
        tx_hash = nft_marketplace.functions.endAuction(end_auction_token_id).transact({'from': account})
        st.write(f'Auction ended for Token ID {end_auction_token_id}. Transaction Hash: {tx_hash.hex()}')