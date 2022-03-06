from src.request_api import  get_point, get_data
import pytest


def test_get_point():
    result = get_point('moscow')
    assert result == (55.75706, 37.60976)


def test_get_data():
    result = get_data(2000, 'moscow')
    assert len(result) > 100
