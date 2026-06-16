from categorize import categorize


def test_dining():
    assert categorize('Blue Bottle Coffee') == 'Food'


def test_subscriptions():
    assert categorize('Netflix monthly') == 'Subscriptions'


def test_transport():
    assert categorize('Uber trip downtown') == 'Transport'


def test_uber_eats_is_food():
    assert categorize('Uber Eats order') == 'Food'


def test_plain_uber_ride_is_transport():
    assert categorize('Uber ride') == 'Transport'


def test_groceries():
    assert categorize('Whole Foods Market') == 'Food'


def test_income():
    assert categorize('ACME Corp payroll') == 'Income'


def test_unknown_falls_back_to_other():
    assert categorize('Mystery vendor 123') == 'Other'
