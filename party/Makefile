all: clean build test deploy

clean:
	rm -rf artifacts/

build:
	npx hardhat compile

test:
	npx hardhat test

deploy:
	npx hardhat run scripts/deploy.ts --network rinkeby

help:
	@echo "make clean/build/deploy/test"

.PHONY: all test clean help