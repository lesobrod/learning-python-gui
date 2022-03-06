from src.request_api import myf, get_point, get_data


# def test_get_point():
#     result = get_point('moscow')
#     print(result)
#     assert result == (55.75706, 37.60976)

def test_myf():
    assert myf() == 1