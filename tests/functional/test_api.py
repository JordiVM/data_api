from data_api import create_app
from data_api.data.api import conversationPool


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
    THEN check that the response is valid and message is stored in db
    """
    app = create_app("flask_test.cfg")

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        post_path = "/data/0/1"
        data = {"text": "Some example text", "language": "EN"}
        response = test_client.post(post_path, data=data)
        assert response.status_code == 200
        assert conversationPool[1].messages[-1].text == "Some example text"
        assert conversationPool[1].messages[-1].language == "EN"
