import { ethers } from "hardhat";
import * as fs from "fs";

async function main() {
    const factory = await ethers.getContractFactory("Will"); // Counter/Will
    // If we had constructor arguments, they would be passed into deploy()
    let contract = await factory.deploy();
    // The address the Contract WILL have once mined
    console.log("Contract address: https://rinkeby.etherscan.io/address/" + contract.address + "#code");
    // The transaction that was sent to the network to deploy the Contract
    console.log("Tx hash: " + contract.deployTransaction.hash);
    // The contract is NOT deployed yet; we must wait until it is mined
    await contract.deployed();

    const data = {
        address: contract.address,
        abi: JSON.parse(contract.interface.format('json').toString())
    };
    fs.writeFileSync('frontend/src/Contract.json', JSON.stringify(data));
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });