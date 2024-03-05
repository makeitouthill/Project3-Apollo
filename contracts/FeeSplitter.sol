// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract FeeSplitter is ReentrancyGuard, Ownable {
  // ApolloToken contract interface
  IERC20 public apolloToken;

  // Addresses for fee distribution
  address public stakingContract;
  address public treasury;
  address public otherBeneficiary; // Example: community fund or charity

  // Fee distribution percentages (must add up to 100%)
  uint256 public stakingShare = 50; // 50%
  uint256 public treasuryShare = 30; // 30%
  uint256 public otherShare = 20; // 20%

  // Event for logging fee distribution
  event FeesDistributed(uint256 totalAmount, uint256 stakingAmount, uint256 treasuryAmount, uint256 otherAmount);

  constructor(address _apolloToken, address _stakingContract, address _treasury, address _otherBeneficiary) Ownable(msg.sender) {
    require(_apolloToken != address(0), "ApolloToken address cannot be zero");
    require(_stakingContract != address(0), "Staking contract address cannot be zero");
    require(_treasury != address(0), "Treasury address cannot be zero");
    require(_otherBeneficiary != address(0), "Other beneficiary address cannot be zero");

      apolloToken = IERC20(_apolloToken);
      stakingContract = _stakingContract;
      treasury = _treasury;
      otherBeneficiary = _otherBeneficiary;
    }

  // Function to distribute fees
  function distributeFees() public nonReentrant onlyOwner {
    uint256 totalBalance = address(this).balance;
    require(totalBalance > 0, "No fees to distribute");

    uint256 stakingAmount = (totalBalance * stakingShare) / 100;
    uint256 treasuryAmount = (totalBalance * treasuryShare) / 100;
    uint256 otherAmount = (totalBalance * otherShare) / 100;

  	// Ensure the total distribution does not exceed the total balance due to rounding
    uint256 totalDistributed = stakingAmount + treasuryAmount + otherAmount;
      if (totalDistributed > totalBalance) {
        // Adjust to prevent overflow
        otherAmount -= totalDistributed - totalBalance;
      }

        // Transfer funds
    	payable(stakingContract).transfer(stakingAmount);
      payable(treasury).transfer(treasuryAmount);
      payable(otherBeneficiary).transfer(otherAmount);

    	emit FeesDistributed(totalBalance, stakingAmount, treasuryAmount, otherAmount);
    }

  // Allow the contract to receive ETH
	receive() external payable {}
}