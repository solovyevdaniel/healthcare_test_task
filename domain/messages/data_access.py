from sqlalchemy import select, insert

from domain import db
from orm_models.models import message_table


class MessagesDao:
    async def get_all(self):
        async with db.session_factory() as session:
            query = select(message_table)
            result = await session.execute(query)
            return [row[1] for row in result.all()]

    async def save_message(self, message, message_type: str):
        async with db.session_factory() as session:
            stmt = insert(message_table).values(
                message=message,
                message_type=message_type,
            )
            await session.execute(stmt)
