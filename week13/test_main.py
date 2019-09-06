from main import sort

def test_empty_list():
    assert [] == sort([]), "empty list is not sorted correctly"