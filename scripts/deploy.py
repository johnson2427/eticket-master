from scripts.contract_setup import ContractSetup
from brownie import TicketExchange, MockV3Aggregator, network, config


class TicketMaster(ContractSetup):
    """
    Class: TicketMaster
    Inherits: ContractSetup

    Deploys the contract to the network, allows for the purchase of a ticket, and for the owner of the contract to
    withdraw funds from the contract

    :param seat: str -> 'bleachers' [accepts: 'front row', 'lower level', 'mid level', 'upper level', 'bleachers']
    functions:
        @staticmethod get_price(:param seat): returns int -> value of seat in USD
        purchase_seat(): returns transaction -> allows for an individual to purchase a ticket
        company_withdraw(): returns None -> allows for the company to withdraw funds from contract
        send_ticket(): returns dict -> following transaction, and confirmation, the ticket is to be sent to the buyer
        deploy_ticket_exchange(): returns ticket_ex -> deploy contract to the network using the owner ID.
    """

    def __init__(self, seat='bleachers'):
        super().__init__()
        self.seat = seat
        self.account = self.get_account()
        self.price = self.get_price(self.seat)
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

    def send_ticket(self):
        print(f"you have purchased a ticket!")
        return {"ticket_type": self.seat,
                "public_key": "TBA"}

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
