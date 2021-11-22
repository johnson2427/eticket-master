# eTicketMaster

#### TicketMaster for the Blockchain

#### Purchase Tickets to sporting events, shows, movies, etc using Ethereum

###### Using Solidity and Python 3.8 [with Brownie]

## Instructions
clone the repository

    git clone https://github.com/johnson2427/eticket-master

create virtual environment (however you wish to do so)

Make sure you install all requirements

    pip install -r requirements.txt

You must create a .env file with the contents below

    export PRIVATE_KEY=YOUR_PRIVATE_KEY
    export WEB3_INFURA_PROJECT_ID=YOUR_INFURA_PROJECT_ID
    export ETHERSCAN_TOKEN=ETHERSCAN_TOKEN

You should be able to run a brownie test from here

    brownie test
    