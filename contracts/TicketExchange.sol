// pay for ticket
// seller withdraws from contract

// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TicketExchange is Ownable{
    mapping(address => uint256) public addressToAmountPaid;
    address[] public ticketsAvailable;
    address[] public purchasers;
    AggregatorV3Interface public priceFeed;
    uint256 ticketPrice;

    constructor(address _priceFeed, uint256 _ticketPrice) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        ticketPrice = _ticketPrice;
    }

    function addTicketsAvailable(address _ticket) public {
        ticketsAvailable.push(_ticket);
    }

    function getTicketPrice() public view returns (uint256){
        return ticketPrice;
    }

    function purchase() public payable {
        uint minimumUSD = ticketPrice * 10**18;
        require(getConversionRate(msg.value) == minimumUSD, "ETH does not match USD!");
        addressToAmountPaid[msg.sender] += msg.value;
        purchasers.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getPurchasePrice() public view returns (uint256) {
        uint256 mimimumUSD = ticketPrice * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (
            uint256 purchaserIndex = 0;
            purchaserIndex < purchasers.length;
            purchaserIndex++
        ) {
            address purchaser = purchasers[purchaserIndex];
            addressToAmountPaid[purchaser] = 0;
        }
        purchasers = new address[](0);
    }

}
