## Dependencies

### Global:
- use nvm to manage node and npm.
- use npm to install all dependencies.
╰ npm list -g
~/.nvm/versions/node/v12.21.0/lib
├── ganache-cli@6.12.2
├── npm@7.6.1
└── yarn@1.22.10
```shell script
npm install -g yarn
npm install -g ganache-cli
```
### NPM --save-dev Dependencies
```shell script
npm install --save-dev hardhat
npm install --save-dev hardhat-typechain typechain ts-generator @typechain/ethers-v5
```

### Run ganache locally
```shell script
ganache-cli --port 8545 --gasLimit 12000000 --accounts 10 --hardfork istanbul --mnemonic brownie --defaultBalanceEther 600
```
