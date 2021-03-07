import { ethers } from "hardhat";
import chai from "chai";
import { solidity } from "ethereum-waffle";
import { Counter } from "../typechain";
chai.use(solidity);
const { expect } = chai;
/**
 * Get an array of pre-funded signers from Ethers.
 Deploy the contracts using the pre-funded signer. Import the Counter type and use it as the type of the variable that gets deployed in the beforeEach.
 Waffle has some useful Chai matchers for writing contract tests like BigNumber matchers and Ethereum address matchers. Check them all out here.
 Simple test to count up and make sure the counter works.
 Those of you that are paying attention will see that this test will fail. Wait on this to see the real magic of Hardhat.
 */
describe("Counter", () => {
    let counter: Counter;
    beforeEach(async () => {
        // 1
        const signers = await ethers.getSigners();
        // 2
        const counterFactory = await ethers.getContractFactory(
            "Counter",
            signers[0]
        );
        counter = (await counterFactory.deploy()) as Counter;
        await counter.deployed();
        const initialCount = await counter.getCount();
        // 3
        expect(initialCount).to.eq(0);
        expect(counter.address).to.properAddress;
    });
    // 4
    describe("count up", async () => {
        it("should count up", async () => {
            await counter.countUp();
            let count = await counter.getCount();
            expect(count).to.eq(1);
        });
    });
    describe("count down", async () => {
        // 5
        // it("should fail", async () => {
        //     // this test will fail
        //     await counter.countDown();
        // });
        it("should count down", async () => {
            await counter.countUp();
            await counter.countDown();
            const count = await counter.getCount();
            expect(count).to.eq(0);
        });
    });
});