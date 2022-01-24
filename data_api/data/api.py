from flask import request
from collections import defaultdict

from data_api.models import Message, Conversation
from data_api.data.blueprint import data_bp

# Hashtable {key=dialogID, value=Conversation}
conversationPool = defaultdict(Conversation)


@data_bp.route("/data/<int:customer_id>/<int:dialog_id>", methods=["POST"])
def post_message(customer_id: int, dialog_id: int):
    text = request.form["text"]
    language = request.form["language"]

    if dialog_id not in conversationPool:
        conversationPool[dialog_id] = Conversation(customer_id, dialog_id)

    conversationPool[dialog_id].add_message(Message(language, text))

    return "", 200
