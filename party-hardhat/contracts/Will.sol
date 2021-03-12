// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.3;

import 'hardhat/console.sol';

contract Will {
    address owner;
    uint fortune;
    bool isGone;

    address payable[] familyWallets; // "payable" allows the address(es) to receive Ether.
    mapping(address => uint) inheritance;

    // 1. This special function will execute automatically upon the contract’s deployment.
    // 2. The “payable” keyword: It allows the function to send and receive ether. The
    // constructor has this modifier so that when we deploy the contract we can initialize
    // it with an ether balance.
    constructor() payable{
        /*
        * @msg.sender, a built-in global variable representative of the address that is calling the function.
        * @msg.value, a built-in variable that tells us how much ether has been sent.
        */
        // i.e. the deploy-er of the contract.
        owner = msg.sender;
        fortune = msg.value;
        isGone = false;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        // tells the execution to shift to the actual function after it finishes reading the modifier.
        _;
    }

    modifier mustBeGone {
        require(isGone == true);
        // tells the execution to shift to the actual function after it finishes reading the modifier.
        _;
    }

    // public but limit it to onlyOwner.
    function setInheritance(address payable wallet, uint inheritAmount) public onlyOwner {
        familyWallets.push(wallet);
        inheritance[wallet] = inheritAmount;
    }

    function payout() private mustBeGone {
        for (uint i = 0; i < familyWallets.length; i++) {
            console.log('Trying to send [%s] to [%s].', inheritance[familyWallets[i]], familyWallets[i]);
            // "transfer()" global method to transfer value
            familyWallets[i].transfer(inheritance[familyWallets[i]]);
            console.log('Owner balance is now [%s] eth.', fortune);
        }
    }

    function gone() public onlyOwner {
        isGone = true;
        payout();
    }
}
