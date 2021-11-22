from scripts.deploy import TicketMaster
from brownie import network, accounts, exceptions
import pytest
import time


def test_can_purchase_and_withdraw():
    tm = TicketMaster()
    transaction = tm.ticket_ex.purchase({"from": tm.account, "value": tm.ticket_fee})
    transaction.wait(1)
    assert tm.ticket_ex.addressToAmountPaid(tm.account.address) == tm.ticket_fee
    withdraw = tm.ticket_ex.withdraw({"from": tm.account})
    withdraw.wait(1)
    assert tm.ticket_ex.addressToAmountPaid(tm.account.address) == 0


def test_only_owner_can_withdraw():
    tm = TicketMaster("front row")
    if network.show_active() not in tm.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    with pytest.raises(ValueError):
        tm.ticket_ex.withdraw({"from": tm.get_account(index=3)})


def test_ticket_master_init():
    tm = TicketMaster("front row")
    assert tm.price == 1200
    assert tm.ticket_fee == 2
