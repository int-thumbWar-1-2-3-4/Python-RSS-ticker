from .context import atomfeed


def test_answer():
    assert atomfeed.atomfeedDemoModule() == 'inside atom feed Demo Module'
