from .context import ams

def test_answer():
    expected = ams.printDemo()
    assert expected == 'inside printDemo'


def test_j():
    assert ams.sum(1) == 5