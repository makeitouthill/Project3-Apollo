require("@nomicfoundation/hardhat-toolbox");
require("@nomicfoundation/hardhat-chai-matchers");
require("@nomicfoundation/hardhat-ethers");
require("dotenv").config();

module.exports = {
  solidity: {
    version: "0.8.20", // Ensure this matches the version used in smart contracts
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      chainId: 1337
    },
    // Testnet configuration
    sepolia: {
      url: process.env.SEPOLIA_URL, // Use the Sepolia RPC URL from your .env file
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [] // Use your private key from the .env file
    }
  },
  // Task to get all accounts and log them to the console [npx hardhat accounts]
  tasks: {
    accounts: async (taskArgs, hre) => {
      const accounts = await hre.ethers.getSigners();
      for (const account of accounts) {
        console.log(account.address);
      }
    },
  },
  mocha: {
    timeout: 20000
  }
};