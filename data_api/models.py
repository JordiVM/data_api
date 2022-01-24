from datetime import datetime


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
        self.timestamp = datetime.timestamp(datetime.now())
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
