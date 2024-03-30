from dataclasses import dataclass
from typing import List


@dataclass
class NewsContent:
    title: str
    timestamp: str
    full_text: str
    tags: str
    author: str
    url: str
    
    @staticmethod
    def new_from_array(data: list):
        return NewsContent(
            title=data[0],
            timestamp=data[1],
            full_text=data[2],
            tags=data[3],
            author=data[4],
            url=data[5],
        )

    @staticmethod
    def header() -> List[str]:
        return [
            'Title',
            'Timestamp',
            'FullText',
            'Tags',
            'Author',
            'Url',
            ]
    
    def to_list(self) -> List[str]:
        return [
            self.title, 
            self.timestamp, 
            self.full_text, 
            self.tags,
            self.author,
            self.url, 
            ]
