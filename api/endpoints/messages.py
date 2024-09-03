from fastapi import APIRouter
from pydantic import Field, BaseModel

from domain.messages.data_access import MessagesDao
from domain.messages.service import MessageService

router = APIRouter(prefix='/messages')

class SaveMessageRequest(BaseModel):
    text: str = Field(examples=["""MSH|^~\&|SENDING_APPLICATION|SENDING_FACILITY|RECEIVING_APPLICATION|RECEIVING_FACILITY|20110613083617||ADT^A01|934576120110613083617|P|2.3||||
EVN|A01|20110613083617|||
PID|1||135769||MOUSE^MICKEY^||19281118|M|||123 Main St.^^Lake Buena Vista^FL^32830||(407)939-1289^^^theMainMouse@disney.com|||||1719|99999999||||||||||||||||||||
PV1|1|O|||||^^^^^^^^|^^^^^^^^"""])


@router.post('/')
async def save_message(message: SaveMessageRequest):
    message_service = MessageService()
    await message_service.save_message(message.text)
    return {"status": "success"}

@router.get('/')
async def get_all_messages():
    message_service = MessageService()
    messages = await message_service.get_all()
    return messages
