from source import Source

class Item:
    def __init__(self, url, source, is_mp3, response):
        self.url = url
        self.source = source
        self.is_mp3 = is_mp3
        self.response = response