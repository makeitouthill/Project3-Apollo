const Web3 = require('web3');
const fs = require('fs');
const path = require('path');
const contractAddress = '0x5FbDB2315678afecb367f032d93F642f64180aa3';

// Initialize web3 with a provider
const web3 = new Web3('http://127.0.0.1:8545');

// Load contract ABI
const contractPath = path.resolve(__dirname, '../src/Marketplace.json');
const contractJson = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
const contractABI = contractJson.abi;

// Create contract instance
const contract = new web3.eth.Contract(contractABI, contractAddress);

// Specify the token ID
const tokenId = 1;

// Query for the tokenURI
contract.methods.tokenURI(tokenId).call()
.then((tokenURI) => {
  console.log(`Metadata URL for token ID ${tokenId}: ${tokenURI}`);
})
.catch((error) => {
  console.error(error);
});