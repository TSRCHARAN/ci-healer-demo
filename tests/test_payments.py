import os

from shop.payments import PaymentsClient


def test_charge_against_sandbox():
    # Needs the payments sandbox key, which CI has never been given.
    client = PaymentsClient(api_key=os.environ["PAYMENTS_API_KEY"])
    assert client.charge(1999)["status"] == "ok"
