import pytest
from vector_math import find_lines_intersection

def test_find_lines_intersection():
    assert find_lines_intersection((0, 0), (1, 1), (0, 1), (1, 0)) == (0.5, 0.5)
    assert find_lines_intersection((0, 0), (1, 1), (0, 1), (1, 1)) == None
    assert find_lines_intersection((0, 0), (1, 1), (0.01, 0), (1, 2)) == (0.5, 0.5)
    
if __name__ == "__main__":
    pytest.main()