// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ApolloStaking is ReentrancyGuard, Ownable {
  using SafeERC20 for IERC20;
    
  IERC20 public immutable ApolloToken;

  uint256 public totalStaked;
  uint256 public rewardRate;
  // Struct to track each user's stake and rewards that is creditted to the User
  struct StakeInfo {
    uint256 amount;
    uint256 rewardDebt;
  }

  mapping(address => StakeInfo) public stakes;

  // Events for tracking staking activities
  // Event recorded when a user stakes tokens into the contract.
  event Staked(address indexed user, uint256 amount);
  // Event recorded when a user unstakes tokens from the contract.
  event Unstaked(address indexed user, uint256 amount);
  // Event recorded when rewards are paid out to a user.
  event RewardPaid(address indexed user, uint256 reward);
  // Event recorded when the reward rate is updated.
  event RewardRateUpdated(uint256 newRewardRate);
    
  // Initializes the contract, setting up the staking token and the initial reward rate.
  // Uses Ownable contract from OpenZeppelin to allow only owner to call functions marked with "onlyOwner"
  constructor(address _ApolloToken, uint256 _rewardRate) Ownable(msg.sender) {
    require(_ApolloToken != address(0), "ApolloToken address cannot be zero");
    ApolloToken = IERC20(_ApolloToken);
    rewardRate = _rewardRate;
  }
}