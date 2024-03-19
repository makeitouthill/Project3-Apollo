# Apollo NFT Marketplace


## Introduction
Apollo NFT Marketplace is a decentralized application that allows users to mint, list, and trade NFTs on the Ethereum blockchain. Built with Solidity, Hardhat, and Streamlit, it provides a seamless experience for both creators and collectors.

# Prerequisites
## Before running the application, ensure you have the following installed:

Node.js (v14.x or above)  
Python (v3.8 or above)  
Hardhat  
Streamlit  
Anaconda  
# Installation  
## Follow these steps to set up the project environment:

1. Node.js Dependencies 
<br> 
`npm install`  
Installs the necessary Node.js packages defined in package.json.
<br>
2. Python Dependencies
<br>
`pip install -r requirements.txt`  
Installs the necessary Python packages defined in requirements.txt. Ensure you're within the correct Python virtual environment or Conda environment.  
<br>
3. Start Hardhat Local Network
<br>
`npx hardhat node`  
Initializes a local Ethereum network for development. Open an Anaconda terminal, navigate to the project folder, and run this command.  
<br>
4. Compile Smart Contracts
<br>
`npx hardhat compile` 
Compiles the smart contracts. Perform this step in a new Anaconda terminal with the blockchain environment activated.  
<br>
5. Deploy Smart Contracts
<br>
`npx hardhat run scripts/deploy.js --network localhost`  
Deploys your smart contracts to the local Ethereum network.  
<br>
6. Environment Variables  
Set up a sample.env file with the necessary configurations (e.g., API keys, private keys) and rename it to .env.  
<br>
6. Streamlit Configuration  
Create a .streamlit folder in the root directory (where app.py resides). Inside, create a file named config.toml with the following content:  
`[server]`  
`enableCORS = false`  
`enableXsrfProtection = false`  
These settings are for development purposes only and should not be used in production.  
<br>
7. Run Streamlit App
<br>
`streamlit run app.py`  
Launches the Streamlit web interface for interacting with the NFT marketplace.
<br>

## Usage
After completing the installation steps, visit http://localhost:8501 in your web browser to interact with the Apollo NFT Marketplace. Here, you can mint new NFTs, list them for sale, and view the NFT gallery.

### Features
- Mint NFTs with custom metadata.  
- List and manage NFTs on the marketplace.  
- Load Total Nft supply, and display them in the NFT Gallery.  
- Interactive UI for a friendly user experience.  
<br>

## Contributing
Unless member of group or instructional Team for this project please no contributions.  Thank you for your understanding.  
<br>

### License
Distributed under the MIT License. See LICENSE for more information.

### Contact
Project Link: https://github.com/makeitouthill/Project3-Apollo