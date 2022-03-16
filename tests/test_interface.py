from pipeline.interface import parse_args
import pytest


def test_parse_args():
    # is the output a list
    assert isinstance(parse_args(["Tropical aquariums"]).book_title, list)
    # is there is only one element in the list
    assert len(parse_args(["Tropical aquariums"]).book_title) == 1
    # is exactly one argument accepted
    with pytest.raises(SystemExit):
        parse_args(["Tropical aquariums", "YOLO"])
    with pytest.raises(SystemExit):
        parse_args([])
