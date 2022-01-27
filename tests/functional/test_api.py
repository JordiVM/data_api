import json

from data_api import create_app
from data_api.data.api import conversationPool
from data_api.models import MessageEntry
from data_api import db
from data_api.utils import random_string


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 404


def test_post_message():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/data/<customer_id>/<dialog_id>' page receive data (POST)
    THEN check that the response is valid and message is stored in structure
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        dialog_id = 10
        post_path = "/data/1/" + str(dialog_id)
        random_text = random_string(50)
        random_language = random_string(10)
        data = {"text": random_text, "language": random_language}
        response = test_client.post(post_path, data=data)
        assert response.status_code == 200
        assert conversationPool[10].messages[-1].text == random_text
        assert conversationPool[10].messages[-1].language == random_language


def test_post_consent_true():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/consent/<dialog_id>' page receive data (POST) with payload true
    THEN check that the response is valid and data stored in db
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        dialog_id = 2
        post_path = "/data/0/" + str(dialog_id)
        random_text = random_string(50)
        random_language = random_string()
        data = {"text": random_text, "language": random_language}
        response = test_client.post(post_path, data=data)
        post_path = "/consents/" + str(dialog_id)
        data = {"consent": "true"}
        response = test_client.post(post_path, data=data)
        assert response.status_code == 200

        # Query db to make sure the conversation has been stored
        query = (
            db.session.query(MessageEntry)
            .order_by(MessageEntry.date)
            .filter((MessageEntry.language == random_language))
            .first()
        )

        assert query.language == random_language


def test_post_consent_false():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/consent/<dialog_id>' page receive data (POST) with payload false
    THEN check that the response is valid and data NOT stored in db
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        dialog_id = 5
        post_path = "/data/0/" + str(dialog_id)
        random_text = random_string(50)
        random_language = random_string()
        data = {"text": random_text, "language": random_language}
        response = test_client.post(post_path, data=data)
        post_path = "/consents/" + str(dialog_id)
        data = {"consent": "false"}
        response = test_client.post(post_path, data=data)
        assert response.status_code == 200

        # Query db to make sure the conversation has been stored
        query = (
            db.session.query(MessageEntry)
            .order_by(MessageEntry.date)
            .filter((MessageEntry.language == random_language))
            .all()
        )

        assert query == []


def test_get_data_language():
    """
    GIVEN a Flask application configured for testing
    WHEN '/data/?language=:language' is requested (GET)
    THEN check that the response is valid and data is retrieved from db
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        dialog_id = 3
        post_path = "/data/0/" + str(dialog_id)
        random_text = random_string(50)
        random_language = random_string()
        data = {"text": random_text, "language": random_language}
        response = test_client.post(post_path, data=data)
        post_path = "/consents/" + str(dialog_id)
        data = {"consent": "true"}
        response = test_client.post(post_path, data=data)
        post_path = "/data/?language=" + random_language
        response = test_client.get(post_path)
        assert response.status_code == 200
        assert random_language in response.data.decode("UTF-8")
        assert random_text in response.data.decode("UTF-8")


def test_get_data_customer_id():
    """
    GIVEN a Flask application configured for testing
    WHEN '/data/?customerId=:customerId' is requested (GET)
    THEN check that the response is valid and data is retrieved from db
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        dialog_id = 6
        customer_id = 1
        post_path = "/data/" + str(customer_id) + "/" + str(dialog_id)
        random_text = random_string(50)
        random_language = random_string(10)
        data = {"text": random_text, "language": random_language}
        response = test_client.post(post_path, data=data)
        post_path = "/consents/" + str(dialog_id)
        data = {"consent": "true"}
        response = test_client.post(post_path, data=data)
        post_path = "/data/?customerId=" + str(customer_id)
        response = test_client.get(post_path)
        assert response.status_code == 200
        assert random_text in response.data.decode("UTF-8")


def test_get_data_bad_request():
    """
    GIVEN a Flask application configured for testing
    WHEN '/data/?something=:something' is requested (GET) Bad Request
    THEN check that the response is 400 invalid
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        post_path = "/data/?something=something"
        response = test_client.get(post_path)
        assert response.status_code == 400


def test_get_missing_language():
    """
    GIVEN a Flask application configured for testing
    WHEN '/data/?language=:language' requested (GET) with language not in db
    THEN check that the response is 200 valid and data is empty str
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        random_language = random_string(10)
        post_path = "/data/?language=" + random_language
        response = test_client.get(post_path)
        assert response.status_code == 200
        assert response.data.decode("UTF-8") == ""


def test_get_multiple_messages():
    """
    GIVEN a Flask application configured for testing
    WHEN '/data/?language=:language' is requested (GET) with multiple entries
    THEN check that the data retrieved from db is descending ordered by date
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        dialog_id = 8
        post_path = "/data/0/" + str(dialog_id)
        random_language = random_string()
        for _ in range(10):
            random_text = random_string(50)
            data = {"text": random_text, "language": random_language}
            response = test_client.post(post_path, data=data)
        post_path = "/consents/" + str(dialog_id)
        data = {"consent": "true"}
        response = test_client.post(post_path, data=data)
        post_path = "/data/?language=" + random_language
        response = test_client.get(post_path)
        assert response.status_code == 200
        response_dict = json.loads(response.data.decode("UTF-8"))
        for i in range(8):
            assert response_dict[i]["date"] >= response_dict[i + 1]["date"]
