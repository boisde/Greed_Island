import { ethers } from "hardhat";
import chai from "chai";
// import { solidity } from "ethereum-waffle";
import { Will } from "../typechain";
import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/dist/src/signer-with-address";
// chai.use(solidity);
const { expect } = chai;

describe('Will', () => {
    let will: Will;
    let owner: SignerWithAddress;

    beforeEach(async () => {
        const signers = await ethers.getSigners();
        owner = signers[0];
        const willFactory = await ethers.getContractFactory('Will', signers[0]);
        will = (await willFactory.deploy()) as Will;
        await will.deployed();
        expect(will.address).to.properAddress;
    });

    describe('Deployment', () => {
        it('should set the right owner', async () => {
            expect("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266").to.equal(owner.address);
        });
    });
});