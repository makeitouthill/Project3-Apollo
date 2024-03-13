from utils.web3_utils import mint_nft
import os

# Replace these values with your actual data
seller_private_key = os.getenv("SELLER_PRIVATE_KEY")
metadata_ipfs_hash = "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH"
token_uri = f"https://ipfs.io/ipfs/{metadata_ipfs_hash}"
price = "0.1"  # NFT price in ETH

# Call the mint_nft function
receipt = mint_nft(token_uri, price, seller_private_key)

if receipt:
    print(f"Transaction hash: {receipt.transactionHash.hex()}")
    print("NFT minted successfully!")
else:
    print("Failed to mint NFT.")