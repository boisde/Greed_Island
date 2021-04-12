require("dotenv").config();
const replace = require("replace-in-file");

import { HardhatUserConfig } from "hardhat/types";
import "@nomiclabs/hardhat-waffle";
import "@nomiclabs/hardhat-etherscan"
import "hardhat-typechain";
import "hardhat-gas-reporter"

const config: HardhatUserConfig = {
    defaultNetwork: "hardhat",
    solidity: {
        compilers: [{ version: "0.7.3", settings: {} }],
        overrides: {
            "contracts/Papi.sol": {
                version: "0.7.6",
                settings: {}
            },
            "contracts/provableAPI_0.7.sol": {
                version: "0.7.6",
                settings: {}
            }
        }
    },
    networks: {
        hardhat: {},
        rinkeby: {
            url: `https://rinkeby.infura.io/v3/${process.env.INFURA_API_KEY}`,
            accounts: [`${process.env.RINKEBY_PRIVATE_KEY}`],
        },
    },
    etherscan: {
        // Obtain one at https://etherscan.io/
        apiKey: process.env.ETHERSCAN_API_KEY,
    },
    gasReporter: {
        currency: 'CNY',
        gasPrice: 1,
    }
};
export default config;