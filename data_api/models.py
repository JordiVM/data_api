from datetime import datetime


class Message:
    def __init__(self, language, text):
        self.timestamp = datetime.timestamp(datetime.now())
        self.language = language
        self.text = text


class Conversation:
    def __init__(self, customer_id, dialog_id):
        self.customer_id = customer_id
        self.dialog_id = dialog_id
        self.messages = []
