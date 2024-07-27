""""""

import re
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
import warnings

import pycrfsuite
from .resources import MODEL_PATH, MODEL_FILE, DIRECTIONS, STREET_NAMES, re_tokens
from .errors import RepeatedLabelError

# The address components are based upon the `United States Thoroughfare,
# Landmark, and Postal Address Data Standard
# http://www.urisa.org/advocacy/united-states-thoroughfare-landmark-and-postal-address-data-standard


try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(MODEL_PATH)
except IOError:
    warnings.warn(
        "You must train the model (parserator train --trainfile "
        "FILES) to create the %s file before you can use the parse "
        "and tag methods" % MODEL_FILE
    )


def parse(address_string: str) -> List[Tuple[str, str]]:
    """
    Parse an address string and return a list of tuples containing
    the tokens and their corresponding labels.

    Args:
        address_string (str): The address string to parse.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the
        tokens and their corresponding labels.
    """
    tokens: List[str] = tokenize(address_string)

    if not tokens:
        return []

    features: List[Dict[str, Union[str, int]]] = tokens_to_features(tokens)
    # print(tokens, features)

    tags: list = TAGGER.tag(features)
    return list(zip(tokens, tags))


def tag(address_string: str, tag_mapping: Optional[dict] = None):
    tagged_address: dict = {}

    last_label = None
    is_intersection = False
    og_labels = []

    parsed = parse(address_string)
    for token, label in parsed:
        if label == "IntersectionSeparator":
            is_intersection = True
        if "StreetName" in label and is_intersection:
            label = "Second" + label

        # saving old label
        og_labels.append(label)
        # map tag to a new tag if tag mapping is provided
        if tag_mapping and label in tag_mapping:
            label = tag_mapping[label]

        if label == last_label:
            tagged_address[label].append(token)
        elif label not in tagged_address:
            tagged_address[label] = [token]
        else:
            raise RepeatedLabelError(address_string, parsed, label)

        last_label = label

    tagged_address = {
        label: " ".join(token).strip(" ,;") for label, token in tagged_address.items()
    }

    return tagged_address, get_address_type(og_labels, is_intersection)


def get_address_type(labels: List[str], intersection: bool) -> str:
    """Get the address type"""
    labels_set = set(labels)
    if "AddressNumber" in labels_set and not intersection:
        return "Street Address"
    if intersection and "AddressNumber" not in labels_set:
        return "Intersection"
    if "USPSBoxID" in labels_set:
        return "PO Box"
    return "Ambiguous"


def tokenize(address_string: str) -> list:
    """Tokenize an address string"""
    if isinstance(address_string, bytes):
        address_string = str(address_string, encoding="utf-8")
    address_string = re.sub(r"(&#38;)|(&amp;)", "&", address_string)

    tokens = re_tokens.findall(address_string)

    if not tokens:
        return []

    return tokens


def token_features(token: str) -> Dict[str, Any]:
    """Token features"""
    token_clean = (
        token
        if token in ("&", "#", "½")
        else re.sub(r"(^[\W]*)|([^.\w]*$)", "", token, flags=re.UNICODE)
    )

    token_abbrev = re.sub(r"[.]", "", token_clean.lower())
    return {
        "abbrev": token_clean.endswith("."),
        "digits": digits(token_clean),
        "word": (token_abbrev if not token_abbrev.isdigit() else False),
        "trailing.zeros": (
            trailing_zeros(token_abbrev) if token_abbrev.isdigit() else False
        ),
        "length": (("d:" if token_abbrev.isdigit() else "w:") + str(len(token_abbrev))),
        "endsinpunc": bool(re.search(r"[^.\w]$", token)),
        "directional": token_abbrev in DIRECTIONS,
        "street_name": token_abbrev in STREET_NAMES,
        "has.vowels": bool(set(token_abbrev[1:]) & set("aeiou")),
    }


def tokens_to_features(address) -> List[Dict[str, Any]]:
    feature_sequence = [token_features(address[0])]
    previous_features = feature_sequence[-1].copy()

    for token in address[1:]:
        token_feats = token_features(token)
        current_features = token_feats.copy()

        feature_sequence[-1]["next"] = current_features
        token_feats["previous"] = previous_features

        feature_sequence.append(token_feats)

        previous_features = current_features

    feature_sequence[0]["address.start"] = True
    feature_sequence[-1]["address.end"] = True

    if len(feature_sequence) > 1:
        feature_sequence[1]["previous"]["address.start"] = True
        feature_sequence[-2]["next"]["address.end"] = True

    return feature_sequence


def digits(
    token: str,
) -> Union[Literal["all_digits"], Literal["some_digits"], Literal["no_digits"]]:
    """Returns 'all_digits', 'some_digits', or 'no_digits'"""
    if token.isdigit():
        return "all_digits"
    if any(char.isdigit() for char in set(token)):
        return "some_digits"
    return "no_digits"


def trailing_zeros(token: str) -> str:
    """Returns the trailing zeros in a token"""
    return "0" * (len(token) - len(token.rstrip("0")))
