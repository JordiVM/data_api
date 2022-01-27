from flask import request
from collections import defaultdict

from data_api.models import Message, Conversation, MessageEntry
from data_api.data import data_bp
from data_api import db

# Hashtable {key=dialogID, value=Conversation}
# Assumes dialogID is unique for all conversations
conversationPool = defaultdict(Conversation)


@data_bp.route("/data/<int:customer_id>/<int:dialog_id>", methods=["POST"])
def post_message(customer_id: int, dialog_id: int):
    text = request.form["text"]
    language = request.form["language"]

    if dialog_id not in conversationPool:
        conversationPool[dialog_id] = Conversation(customer_id, dialog_id)

    conversationPool[dialog_id].add_message(Message(language, text))

    return "", 200


@data_bp.route("/consents/<int:dialog_id>", methods=["POST"])
def post_consent(dialog_id: int):
    consent = request.form["consent"]  # assumes consent is str

    if consent == "true":
        for message in conversationPool[dialog_id].messages:
            entry = MessageEntry(
                date=message.timestamp,
                customer_id=conversationPool[dialog_id].customer_id,
                dialog_id=conversationPool[dialog_id].dialog_id,
                text=message.text,
                language=message.language,
            )
            db.session.add(entry)
            db.session.commit()

    conversationPool[dialog_id] = None

    return "", 200


@data_bp.route("/data/", methods=["GET"])
def get_messages():
    language = request.args.get("language")
    customer_id = request.args.get("customerId")

    result = (
        db.session.query(MessageEntry)
        .filter_by(language=language, customer_id=customer_id)
        .all()
    )

    print(result)

    return "", 200
