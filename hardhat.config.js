require('dotenv').config();

require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-ethers");
const fs = require('fs');

task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});

module.exports = {
  defaultNetwork: "hardhat",
  networks: {
    hardhat: {
      chainId: 1337
    },
    //sepolia: {
    //  url: process.env.SEPOLIA_URL, // Use the Sepolia RPC URL from your .env file
    //  accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [] // Use your private key from the .env file
    //}
  },
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  }
};