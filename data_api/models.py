from datetime import datetime


class Message:
    def __init__(self, language, text):
        self.timestamp = datetime.timestamp(datetime.now())
        self.language = language
        self.text = text
