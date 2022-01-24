from data_api.models import Message, Conversation


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
