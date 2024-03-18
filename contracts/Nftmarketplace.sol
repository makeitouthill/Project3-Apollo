// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract NFTMarketplace is ERC721URIStorage {
    uint256 private _tokenIds = 0;
    uint256 private _itemsSold = 0;

    address payable owner;
    uint256 listingPrice = 0.01 ether;

    struct ListedToken {
        uint256 tokenId;
        address payable owner;
        address payable seller;
        uint256 price;
        bool currentlyListed;
    }

    struct Auction {
        uint256 tokenId;
        address payable seller;
        uint256 minPrice;
        uint256 endTime;
        address highestBidder;
        uint256 highestBid;
        bool ended;
    }

    mapping(uint256 => ListedToken) private idToListedToken;
    mapping(uint256 => Auction) public auctions;

    event TokenListedSuccess(
        uint256 indexed tokenId,
        address owner,
        address seller,
        uint256 price,
        bool currentlyListed
    );

    event AuctionCreated(
        uint256 indexed tokenId,
        address seller,
        uint256 minPrice,
        uint256 endTime
    );

    event NewBid(
        uint256 indexed tokenId,
        address bidder,
        uint256 bid
    );

    event AuctionEnded(
        uint256 indexed tokenId,
        address winner,
        uint256 winningBid
    );

    constructor() ERC721("NFTMarketplace", "NFTM") {
        owner = payable(msg.sender);
    }

    function updateListingPrice(uint256 newListingPrice) public payable {
        require(owner == msg.sender, "Only marketplace owner can update listing price");
        listingPrice = newListingPrice;
    }

    function getListingPrice() public view returns (uint256) {
        return listingPrice;
    }
    function totalSupply() public view returns (uint256) {
    return _tokenIds;
}
    function createToken(string memory tokenURI, uint256 price) public payable returns (uint) {
        _tokenIds += 1;
        uint256 newTokenId = _tokenIds;

        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        createListedToken(newTokenId, price);

        return newTokenId;
    }

    function createListedToken(uint256 tokenId, uint256 price) private {
        require(msg.value == listingPrice, "Price must be equal to listing price");
        require(price > 0, "Price must be greater than zero");

        idToListedToken[tokenId] = ListedToken(
            tokenId,
            payable(address(this)),
            payable(msg.sender),
            price,
            true
        );

        _transfer(msg.sender, address(this), tokenId);
        emit TokenListedSuccess(
            tokenId,
            address(this),
            msg.sender,
            price,
            true
        );
    }

    function executeSale(uint256 tokenId) public payable {
        uint price = idToListedToken[tokenId].price;
        address seller = idToListedToken[tokenId].seller;
        require(msg.value == price, "Please submit the asking price in order to complete the purchase");

        idToListedToken[tokenId].currentlyListed = false;
        idToListedToken[tokenId].seller = payable(msg.sender);
        _itemsSold++;

        _transfer(address(this), msg.sender, tokenId);
        payable(owner).transfer(listingPrice);
        payable(seller).transfer(msg.value);
    }

    // Auction functions
    function createAuction(uint256 tokenId, uint256 minPrice, uint256 duration) public {
        require(msg.sender == ownerOf(tokenId), "Only the owner can create an auction");
        require(duration > 0, "Duration must be greater than zero");

        auctions[tokenId] = Auction(
            tokenId,
            payable(msg.sender),
            minPrice,
            block.timestamp + duration,
            address(0),
            0,
            false
        );

        emit AuctionCreated(tokenId, msg.sender, minPrice, block.timestamp + duration);
    }

    function bid(uint256 tokenId) public payable {
        Auction storage auction = auctions[tokenId];
        require(block.timestamp < auction.endTime, "Auction has ended");
        require(msg.value > auction.highestBid, "Bid must be higher than the current highest bid");

        if (auction.highestBidder != address(0)) {
            // Refund the previous highest bidder
            payable(auction.highestBidder).transfer(auction.highestBid);
        }

        auction.highestBidder = msg.sender;
        auction.highestBid = msg.value;

        emit NewBid(tokenId, msg.sender, msg.value);
    }

    function endAuction(uint256 tokenId) public {
        Auction storage auction = auctions[tokenId];
    require(block.timestamp >= auction.endTime, "Auction has not ended yet");

    auction.ended = true;

    if (auction.highestBidder != address(0)) {
        emit AuctionEnded(tokenId, auction.highestBidder, auction.highestBid);
        _transfer(ownerOf(tokenId), auction.highestBidder, tokenId);
    } else {
        _transfer(address(this), ownerOf(tokenId), tokenId);
    }
    }
} 
