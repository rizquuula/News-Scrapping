import pytest
from NewsScraper.models.news import NewsContent


@pytest.mark.parametrize('arr', (
    (['title', 'timestamp', 'full_text', 'tags', 'author', 'url']),
))
def test_news_should_success(arr):
    nc = NewsContent.new_from_array(arr)
    assert nc.title == arr[0]
    assert nc.timestamp == arr[1]
    assert nc.full_text == arr[2]
    assert nc.tags == arr[3]
    assert nc.author == arr[4]
    assert nc.url == arr[5]
    
    assert nc.header() == ['Title', 'Timestamp', 'FullText', 'Tags', 'Author', 'Url']
    
    assert len(arr) == len(nc.to_list())
    assert all([a == b for a, b in zip(arr, nc.to_list())])


@pytest.mark.parametrize('arr', (
    (['title', 'timestamp', 'full_text', 'tags', 'author']),
))
def test_news_should_raise_wrong_length(arr):
    with pytest.raises(ValueError) as e:
        NewsContent.new_from_array(arr)
    assert str(e.value) == 'the length of array should be 6. (title, timestamp, full_text, tags, author, url)'
    