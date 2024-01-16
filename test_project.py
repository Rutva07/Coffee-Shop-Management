import pytest
from project import requirement, isvalid, verify_email


def test_requirement(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')
    assert requirement() == "1"
    monkeypatch.setattr('builtins.input', lambda _: '2')
    assert requirement() == "2"
    monkeypatch.setattr('builtins.input', lambda _: '4')
    assert requirement() == "4"


def test_isvalid():
    assert isvalid("expresso") == True
    assert isvalid("dog") == False
    assert isvalid("latte") == True
    assert isvalid("monkey") == False
    assert isvalid("12345") == False


def test_verify_email():
    assert verify_email("cat.dog@coffee.com") == True
    assert verify_email("cat.dog@gamil.com") == False
    assert verify_email("cat.DOG@coffee.com") == True
    assert verify_email("cat@dog@coffee.com") == False