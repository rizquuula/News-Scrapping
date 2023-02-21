class News:
    Title: str
    Timestamp: str
    FullText: str
    Tags: str
    Author: str
    Url: str

    def header(self):
        return [
            'Title',
            'Timestamp',
            'FullText',
            'Tags',
            'Author',
            'Url',
            ]
    
    def to_list(self):
        return [
            self.Title, 
            self.Timestamp, 
            self.FullText, 
            self.Tags,
            self.Author,
            self.Url, 
            ]

class Progress:
    Filename: str
    LastId: int
