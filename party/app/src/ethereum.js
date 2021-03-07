import {Contract, ethers} from 'ethers';
import SomeContract from './Contract.json';

const getBlockchain = () =>
    new Promise((resolve, reject) => {
        window.addEventListener('load', async () => {
            if (window.ethereum) {
                await window.ethereum.enable();
                const provider = new ethers.providers.Web3Provider(window.ethereum);
                const signer = provider.getSigner();
                const signerAddress = await signer.getAddress();
                const token = new Contract(
                    SomeContract.address,
                    SomeContract.abi,
                    signer
                );

                resolve({signerAddress, token});
            }
            resolve({signerAddress: undefined, token: undefined});
        });
    });

export default getBlockchain;