from datetime import datetime

from domain.converters.base import BaseMessageConverter
from domain.converters.models.hl7 import HL7Message, HL7PatientVisitSegment, HL7PatientIdentificationSegment, Address, \
    EventType, Hl7EventSegment, MessageType, Hl7HeaderSegment
from hl7apy.parser import parse_message


class RawMessageToHl7Ad01Converter(BaseMessageConverter):
    def convert(self, raw_message: str) -> HL7Message:
        hl7_message = raw_message.replace("\n", "\r")
        parsed_message = parse_message(hl7_message)

        if not parsed_message.validate():
            raise ValueError("Invalid HL7 message")

        header = self._get_header(parsed_message.MSH)
        event = self._get_event(parsed_message.EVN)
        patient = self._get_patient(parsed_message.PID)
        visit = self._get_visit(parsed_message.PV1)

        return HL7Message(
            header=header,
            event=event,
            patient=patient,
            visit=visit,
        )

    def _get_header(self, msh):
        return Hl7HeaderSegment(
            sending_application=msh.MSH_3.value,
            sending_facility=msh.MSH_4.value,
            receiving_application=msh.MSH_5.value,
            receiving_facility=msh.MSH_6.value,
            created_at=datetime.strptime(msh.MSH_7.value,
                                         "%Y%m%d%H%M%S") if msh.MSH_7.value else None,
            type=MessageType(msh.MSH_9.value.replace("^", "_")),
            control_id=msh.MSH_10.value,
            processing_id=msh.MSH_11.value,
            version_id=msh.MSH_12.value,
            security=msh.MSH_13.value,
            acknowledgment_type=msh.MSH_14.value,
            application_acknowledgment_type=msh.MSH_15.value,
        )

    def _get_event(self, evn):
        return Hl7EventSegment(
            type=EventType(evn.EVN_1.value),
            created_at=datetime.strptime(evn.EVN_2.value,
                                         "%Y%m%d%H%M%S") if evn.EVN_2.value else None,
            modified_at=evn.EVN_3.value or None,
            operation_id=evn.EVN_4.value,
            reason=evn.EVN_5.value,
        )

    def _get_patient(self, pid):
        line, other_address = pid.PID_11.value.split("^^")
        city, state, postal_code = other_address.split("^")
        address = Address(
            line=line,
            city=city,
            state=state,
            postal_code=postal_code,
        )
        return HL7PatientIdentificationSegment(
            set_id=pid.PID_1.value,
            patient_id=pid.PID_3.value,
            name=pid.PID_5.value.replace("^", " "),
            birthdate=datetime.strptime(pid.PID_7.value,
                                        "%Y%m%d") if pid.PID_7.value else None,
            sex=pid.PID_8.value,
            address=address,
            phone=pid.PID_13.value.split("^^^")[0],
            email=pid.PID_13.value.split("^^^")[1],
        )

    def _get_visit(self, pv1):
        return HL7PatientVisitSegment(
            set_id=pv1.PV1_1.value,
            patient_class=pv1.PV1_2.value,
        )
