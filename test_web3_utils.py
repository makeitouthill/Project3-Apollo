from utils.web3_utils import mint_nft

# Replace these values with actual test values applicable to your contract
TEST_TOKEN_URI = "http://ipfs.io/ipfs/QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH"
TEST_PRICE = "0.01"  # Test price for NFT
TEST_SELLER_PRIVATE_KEY = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

def test_mint_nft():
    print("Testing mint_nft function from web3_utils.py")
    receipt = mint_nft(TEST_TOKEN_URI, TEST_PRICE, TEST_SELLER_PRIVATE_KEY)
    
    if receipt:
        print(f"Success! Transaction receipt: {receipt}")
    else:
        print("Minting failed.")

if __name__ == "__main__":
    test_mint_nft()