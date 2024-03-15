// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ApolloToken is ERC20, Ownable {
	//Constructor to mint initial supply to the msg.sender
	constructor(uint256 initialSupply) ERC20("ApolloToken", "APOO") Ownable(msg.sender) {
    _mint(msg.sender, initialSupply);
	}

	//Public function to mint tokens. Only the owner can mint.
	function mint(address to, uint256 amount) public onlyOwner {
		_mint(to, amount);
	}

	//Allows token holders to burn their tokens
	function burn(uint256 amount) public {
		_burn(msg.sender, amount);
	}

	//Bulk transfer function to allow sending tokens to multiple recipients
	function bulkTransfer(address[] calldata recipients, uint256[] calldata amounts) public {
		require(recipients.length == amounts.length, "Recipients and amounts length mismatch");
		for (uint256 i = 0; i < recipients.length; i++) {
			_transfer(msg.sender, recipients[i], amounts[i]);
		}
	}
}