/**
 * @type import('hardhat/config').HardhatUserConfig
 */
import { HardhatUserConfig } from "hardhat/types";
import "@nomiclabs/hardhat-waffle";
import "hardhat-typechain";

// module.exports = {
//     solidity: "0.7.3",
// };

let INFURA_API_KEY = "";
let RINKEBY_PRIVATE_KEY = "";
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
};
export default config;

// import { HardhatUserConfig } from "hardhat/types";
// import "@nomiclabs/hardhat-waffle";
// import "hardhat-typechain";
// const config: BuidlerConfig = {
//     solidity: {
//         compilers: [{ version: "0.6.8", settings: {} }],
//     },
// };
// export default config;