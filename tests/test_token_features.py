# -*- coding: utf-8 -*-
from src.usaddress.usaddress import token_features


def test_unicode() -> None:
    features = token_features("å")
    assert features["endsinpunc"] is False
