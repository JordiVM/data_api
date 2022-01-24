from data_api.models import Message


def test_new_message():
    """
    GIVEN a MESSAGE model
    WHEN a new MESSAGE is created
    THEN check the language and date are defined correctly
    """
    message = Message("EN", "A short string that will be a message")
    assert message.language == "EN"
    assert message.text == "A short string that will be a message"
    assert message.timestamp is not None
