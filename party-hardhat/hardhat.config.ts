import { HardhatUserConfig } from "hardhat/types";
import "@nomiclabs/hardhat-waffle";
import "@nomiclabs/hardhat-etherscan"
import "hardhat-typechain";

let INFURA_API_KEY = "3544c4f3208b42ddbe8222256dfd0a66";
let RINKEBY_PRIVATE_KEY = "8ba64ada85d2ebba3af2b0d31035eeb5ded3a88f82b65a2a456ff139c368955e";
let ETHERSCAN_API_KEY = "22BQF61J2MK5ID53YI9AEUNGMD7Z3RMSJ7";
const config: HardhatUserConfig = {
    defaultNetwork: "hardhat",
    solidity: {
        compilers: [{ version: "0.7.3", settings: {} }],
    },
    networks: {
        hardhat: {},
        rinkeby: {
            url: `https://rinkeby.infura.io/v3/${INFURA_API_KEY}`,
            accounts: [RINKEBY_PRIVATE_KEY],
        },
    },
    etherscan: {
        // Obtain one at https://etherscan.io/
        apiKey: ETHERSCAN_API_KEY,
    },
};
export default config;
