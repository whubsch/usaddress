# from parserator.training import readTrainingData
import pytest

from src.usaddress import parse
from src.usaddress.resources import GROUP_LABEL


def equals(addr, labels_pred, labels_true):
    prettyPrint(addr, labels_pred, labels_true)
    assert labels_pred == labels_true


def fuzzyEquals(addr, labels_pred, labels_true):
    fuzzy_labels = []
    for label in labels_pred:
        if label.startswith("StreetName"):
            fuzzy_labels.append("StreetName")
        elif label.startswith("AddressNumber"):
            fuzzy_labels.append("AddressNumber")
        elif label == "Null":
            fuzzy_labels.append("NotAddress")
        else:
            fuzzy_labels.append(label)
    labels = [label for label in labels_true]
    prettyPrint(addr, fuzzy_labels, labels)
    assert fuzzy_labels == labels


# @pytest.mark.parametrize(
#     "test_file",
#     [
#         "measure_performance/test_data/simple_address_patterns.xml",
#         "measure_performance/test_data/labeled.xml",
#     ],
# )
# def test_performance(test_file):
#     data = list(readTrainingData([test_file], GROUP_LABEL))
#     for labeled_address in data:
#         address_text, components = labeled_address
#         _, labels_true = zip(*components)
#         _, labels_pred = zip(*parse(address_text))
#         equals(address_text, labels_pred, labels_true)


# @pytest.mark.parametrize(
#     "test_file",
#     [
#         "measure_performance/test_data/synthetic_osm_data.xml",
#         "measure_performance/test_data/us50_test_tagged.xml",
#     ],
# )
# def test_performance_old(test_file):
#     data = list(readTrainingData([test_file], GROUP_LABEL))
#     for labeled_address in data:
#         address_text, components = labeled_address
#         _, labels_true = zip(*components)
#         _, labels_pred = zip(*parse(address_text))
#         if test_file == "measure_performance/test_data/us50_test_tagged.xml":
#             fuzzyEquals(address_text, labels_pred, labels_true)
#         else:
#             equals(address_text, labels_pred, labels_true)


def prettyPrint(addr, predicted, true):
    print("ADDRESS:    ", addr)
    print("pred:       ", predicted)
    print("true:       ", true)
