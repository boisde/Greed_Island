// SPDX-License-Identifier: MIT
pragma solidity 0.7.6;

import "./provableAPI_0.7.sol";

contract DieselPrice is usingProvable {

    uint256 public dieselPriceUSD;

    event LogNewDieselPrice(string price);
    //    event LogNewProvableQuery(string description);
    //    event LogMyID(bytes32 myID);
    event LogIntDieselPrice(uint256 price);

    constructor()
    {
        update();
        // First check at contract creation...
    }

    function __callback(
        bytes32 _,
        string memory _result
    )
    public
    override
    {
        require(msg.sender == provable_cbAddress());
        emit LogNewDieselPrice(_result);
        //        emit LogMyID(_myID);
        dieselPriceUSD = parseInt(_result, 2);
        // 3.16*100
        emit LogIntDieselPrice(dieselPriceUSD);
        // Let's save it as cents...
        // Now do something with the USD Diesel price...
    }

    function update()
    public
    payable
    {
        //        emit LogNewProvableQuery("Provable query was sent, standing by for the answer...");
        provable_query("URL", "xml(https://www.fueleconomy.gov/ws/rest/fuelprices).fuelPrices.diesel");
    }
}