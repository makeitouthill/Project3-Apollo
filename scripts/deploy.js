const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
  const [deployer] = await ethers.getSigners();
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log(`Deploying contracts with the account: ${deployer.address}`);
  console.log(`Account balance: ${ethers.utils.formatEther(balance)} ETH`);

  const Marketplace = await ethers.getContractFactory("NFTMarketplace");
  const marketplace = await Marketplace.deploy();

  await marketplace.deployed();
  console.log(`Contract deployed to address: ${marketplace.address}`);

  const data = {
    address: marketplace.address,
    abi: marketplace.interface.format('json')
  };

  // Ensure the ./src directory exists or handle the error
  if (!fs.existsSync('./src')) {
    fs.mkdirSync('./src', { recursive: true });
  }
  
  // This writes the ABI and address to the mktplace.json
  fs.writeFileSync('./src/Marketplace.json', JSON.stringify(data, null, 2)); // Pretty print JSON
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error:", error);
    process.exit(1);
  });