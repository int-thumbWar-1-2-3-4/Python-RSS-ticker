from .context import rssfeed


def test_answer():
    assert rssfeed.rssFeedDemoModule() == 'inside rss Feed Demo Module'
