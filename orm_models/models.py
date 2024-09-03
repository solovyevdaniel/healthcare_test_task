
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

message_table = Table(
    "message",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", JSONB),
    Column("message_type", String),
)