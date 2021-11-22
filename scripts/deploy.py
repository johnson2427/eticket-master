from scripts.helpful_scripts import ContractSetup
from brownie import TicketExchange, MockV3Aggregator, network, config, accounts


class TicketMaster(ContractSetup):

    def __init__(self, seat='bleachers'):
        super().__init__()
        self.account = self.get_account()
        self.price = self.get_price(seat)
        self.ticket_ex = self.deploy_ticket_exchange()
        self.ticket_fee = self.ticket_ex.getPurchasePrice()

    @staticmethod
    def get_price(seat_type):
        if seat_type == 'front row':
            return 1200
        elif seat_type == 'lower level':
            return 500
        elif seat_type == 'mid level':
            return 200
        elif seat_type == 'upper level':
            return 100
        elif seat_type == 'bleachers':
            return 50
        else:
            return 0

    def purchase_seat(self):
        transaction = self.ticket_ex.purchase({"from": self.account, "value": self.ticket_fee + 100})
        transaction.wait(1)
        return transaction

    def company_withdraw(self):
        withdraw = self.ticket_ex.withdraw({"from": self.account})
        withdraw.wait(1)

    def deploy_ticket_exchange(self):
        if network.show_active() not in self.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
        else:
            self.deploy_mocks()
            price_feed_address = MockV3Aggregator[-1].address
        ticket_ex = TicketExchange.deploy(price_feed_address,
                                          self.price,
                                          {"from": self.account},
                                          publish_source=config["networks"][network.show_active()].get("verify"))
        print(f"Contract deployed to {ticket_ex.address}")
        return ticket_ex


def main():
    tm = TicketMaster()
    tm.deploy_ticket_exchange()
    print("deploy complete")
    print(f"Seat Price [USD]: {tm.price}")
    print(f"Ticket Fee [ETH]: {tm.ticket_fee}")
    print(f"{tm.ticket_ex.getPurchasePrice(), tm.ticket_ex.getPrice(), tm.ticket_ex.getTicketPrice()}")
