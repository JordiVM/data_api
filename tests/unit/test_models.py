from datetime import datetime

from data_api.models import Message, Conversation, MessageEntry
from data_api.utils import random_string


def test_new_message():
    """
    GIVEN a MESSAGE model
    WHEN a new MESSAGE is created
    THEN check language, text and date are defined correctly
    """
    message = Message("EN", "A short string that will be a message")
    assert message.language == "EN"
    assert message.text == "A short string that will be a message"
    assert message.timestamp is not None


def test_new_Conversation():
    """
    GIVEN a Conversation model
    WHEN a new CONVERSATION is created
    THEN check customer_id, dialog_id and messages are defined correctly
    """
    conversation = Conversation(2, 10)
    assert conversation.customer_id == 2
    assert conversation.dialog_id == 10
    assert conversation.messages == []


def test_add_message():
    """
    GIVEN a Conversation model
    WHEN a new message is added
    THEN check message is added at the end of the list
    """
    conversation = Conversation(3, 10)
    random_text = random_string(50)
    random_language = random_string(10)
    message = Message(random_language, random_text)
    conversation.add_message(message)
    assert conversation.messages[-1].text == random_text
    assert conversation.messages[-1].language == random_language


def test_serialize_entry():
    """
    GIVEN a MessageEntry instance
    WHEN entry has to be serialized
    THEN check columns from MessageEntry are added to the dict
    """
    date = datetime.now()
    customer_id = 1
    dialog_id = 0
    text = "Text to serialize"
    language = "EN"

    entry = MessageEntry(
        date=date,
        customer_id=customer_id,
        dialog_id=dialog_id,
        text=text,
        language=language,
    )

    serialized_entry = entry.serialize()

    assert serialized_entry["date"] == str(date)
    assert serialized_entry["customer_id"] == customer_id
    assert serialized_entry["dialog_id"] == dialog_id
    assert serialized_entry["text"] == text
    assert serialized_entry["language"] == language
