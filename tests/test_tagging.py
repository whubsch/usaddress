from src.usaddress import tag, parse


def test_broadway_tag() -> None:
    """Test that the tag function works"""
    s1 = "1775 Broadway And 57th, New york NY"
    assert tag(s1) == (
        {
            "AddressNumber": "1775",
            "StreetName": "Broadway",
            "IntersectionSeparator": "And",
            "SecondStreetName": "57th",
            "PlaceName": "New york",
            "StateName": "NY",
        },
        "Ambiguous",
    )


def test_broadway_parse() -> None:
    """Test that the parse function works"""
    s1 = "1775 Broadway And 57th, New york NY"
    assert parse(s1) == [
        ("1775", "AddressNumber"),
        ("Broadway", "StreetName"),
        ("And", "IntersectionSeparator"),
        ("57th,", "StreetName"),
        ("New", "PlaceName"),
        ("york", "PlaceName"),
        ("NY", "StateName"),
    ]
