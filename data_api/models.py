from datetime import datetime
from data_api import db


class Message:
    """
    Class to represent a message in the chat

    * timestamp : float - indicates date and time of message creation
    * language : str - language to classify the text in the message
    * text : str - contents of the message
    """

    def __init__(self, language: str, text: str):
        """
        Create a new Message object using language and text
        """
        self.timestamp = datetime.now()
        self.language = language
        self.text = text


class Conversation:
    """
    Class to represent a conversation from the chat

    * customer_id : int - unique ID that identifies the customer that
      engaged in the chat
    * dialog_id : str - ID that identifies the dialog
    * messages : list[Message] - contents of the message
    """

    def __init__(self, customer_id: int, dialog_id: int):
        """
        Create a new Conversation object using customer_id and dialog_id.
        messages will always start empty
        """
        self.customer_id = customer_id
        self.dialog_id = dialog_id
        self.messages = []

    def add_message(self, message: Message):
        """
        Add message to conversation
        """
        self.messages.append(message)


class MessageEntry(db.Model):
    """
    Class to represent a message entry in the db
    """

    __tablename__ = "MESSAGE_ENTRIES"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer)
    dialog_id = db.Column(db.Integer)
    text = db.Column(db.String(200))
    language = db.Column(db.String(50))

    def serialize(self):
        """
        Converts instance MessageEntry to serializable dict
        """
        return {
            "date": str(self.date),
            "customer_id": self.customer_id,
            "dialog_id": self.dialog_id,
            "text": self.text,
            "language": self.language,
        }
