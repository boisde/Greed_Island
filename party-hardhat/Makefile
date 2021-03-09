all: clean build test deploy

clean:
	rm -rf artifacts/
	npx hardhat clean

build:
	npx hardhat compile

test:
	npx hardhat test

deploy:
	npx hardhat run scripts/deploy.ts --network rinkeby

verify:
	@echo "i.e. https://rinkeby.etherscan.io/address/0x5118B1C2B8A64767C142F483cB5AE284675EFE4B#code"
	@echo "npx hardhat verify --contract contracts/Will.sol:Will 0x5118B1C2B8A64767C142F483cB5AE284675EFE4B --network rinkeby"

help:
	@echo "make clean/build/deploy/test"


.PHONY: all test clean help build