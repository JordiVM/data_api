from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    DateTime,
    Text,
)

engine = create_engine("sqlite:///instance/messages.db", echo=True)
meta = MetaData()

chat_entries = Table(
    "message_entries",
    meta,
    Column("id", Integer, primary_key=True),
    Column("date", DateTime),
    Column("customer_id", Integer),
    Column("dialog_id", Integer),
    Column("text", Text),
    Column("language", Text),
)
meta.create_all(engine)
