from web3 import Web3
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the seller's private key from environment variables
seller_private_key = os.getenv('SELLER_PRIVATE_KEY')

# Initialize Web3 connection
WEB3_PROVIDER_URI = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

# Verify if Web3 connection is established
if not web3.isConnected():
  raise Exception("Unable to connect to Web3 provider.")

# Contract details
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Function to load in contract ABI
def load_contract_abi(file_path='src/Marketplace.json'):
  with open(file_path, 'r') as file:
    contract_info = json.load(file)
    return contract_info['abi']

CONTRACT_ABI = load_contract_abi()

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def mint_nft(token_uri, price, seller_private_key):
  seller_address = web3.eth.account.from_key(seller_private_key).address
  balance = web3.eth.get_balance(seller_address)
  print(f"Seller's balance: {web3.from_wei(balance, 'ether')} ETH")

  # Check if balance is sufficient (adjust according to your gas estimation)
  required_balance = web3.to_wei(0.5, 'ether')  # Example value, adjust as necessary
  if balance < required_balance:
    print("Insufficient balance to mint NFT.")
    return None

  nonce = web3.eth.get_transaction_count(seller_address)

  # Preparing transaction
  txn = contract.functions.createToken(token_uri, web3.to_wei(price, 'ether')).build_transaction({
    'chainId': web3.eth.chain_id,
    'gas': 2000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': nonce,
  })

  # Signing transaction
  signed_txn = web3.eth.account.sign_transaction(txn, private_key=seller_private_key)
  
  # Sending transaction
  txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
  
  # Wait for transaction receipt
  txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
  
  return txn_receipt