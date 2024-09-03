from domain.converters.hl7_ad01_to_fhir import Hl7Ad01ToFHIRConverter
from domain.converters.raw_message_to_hl7 import RawMessageToHl7Ad01Converter
from domain.messages.data_access import MessagesDao


class MessageService:
    def __init__(self):
        self._dao = MessagesDao()

    async def get_all(self):
        messages = await self._dao.get_all()
        return messages

    async def save_message(self, raw_message: str):
        hl7_message = RawMessageToHl7Ad01Converter().convert(raw_message)
        fhir_message = Hl7Ad01ToFHIRConverter().convert(hl7_message)
        await self._dao.save_message(fhir_message.json(), "fhir")
