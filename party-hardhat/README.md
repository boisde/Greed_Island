1. install npm dependencies
```bash
npm install --save-dev hardhat-typechain typechain ts-generator @typechain/ethers-v5
npm install --save-dev hardhat
ganache-cli --port 8545 --gasLimit 12000000 --accounts 10 --hardfork istanbul --mnemonic brownie --defaultBalanceEther 600
```