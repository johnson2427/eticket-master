from brownie import accounts, network, config, MockV3Aggregator, Contract


class ContractSetup:

    def __init__(self):
        self.LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
        self.contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}
        self.DECIMALS = 8
        self.STARTING_PRICE = 200000000000

    def get_account(self, index=None, id=None):
        if index:
            return accounts[index]
        if network.show_active() in self.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            return accounts[0]
        if id:
            return accounts.load(id)
        return accounts.add(config["wallets"]["from_key"])

    def get_contract(self, contract_name):
        contract_type = self.contract_to_mock[contract_name]
        if network.show_active() in self.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            if len(contract_type) <= 0:
                self.deploy_mocks()
            contract = contract_type[-1]
        else:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        return contract

    def deploy_mocks(self):
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        if len(MockV3Aggregator) <= 0:
            MockV3Aggregator.deploy(self.DECIMALS, self.STARTING_PRICE, {"from": self.get_account()})
        print("Mocks Deployed!")
