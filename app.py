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
    total_nfts = nft_marketplace.functions.totalSupply().call()
    for i in range(total_nfts):
        token_uri = nft_marketplace.functions.tokenURI(i + 1).call()
        st.image(token_uri, width=200)
        st.write(f'Token ID: {i + 1}')

# List NFT
st.header('List My NFT')
with st.form('List NFT Form'):
    nft_name = st.text_input('NFT Name')
    nft_description = st.text_area('NFT Description')
    nft_price = st.number_input('Price (in ETH)', min_value=0.01)
    nft_image = st.file_uploader('Upload Image (<500 kB)', type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button('List NFT')
    if submitted and nft_image is not None:
        # Upload image to IPFS and get the URI
        image_uri = upload_to_ipfs(nft_image)
        # Create token and list NFT
        account = web3.eth.accounts[0]
        tx_hash = nft_marketplace.functions.createToken(image_uri, web3.toWei(nft_price, 'ether')).transact({'from': account, 'value': web3.toWei(0.01, 'ether')})
        st.write(f'You are listing {nft_name} for {nft_price} ETH. Transaction Hash: {tx_hash.hex()}')

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
