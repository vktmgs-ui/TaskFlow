import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from algorithms import insertion_sort, binary_search, linear_search


def test_insertion_sort():
    data = [5, 2, 4, 1, 3]

    result = insertion_sort(data)

    assert result == [1, 2, 3, 4, 5]


def test_linear_search():
    data = ["task1", "task2", "task3"]

    result = linear_search(data, "task2")

    assert result == "task2"


def test_binary_search():
    data = ["task1", "task2", "task3", "task4"]

    result = binary_search(data, "task3")

    assert result == "task3"