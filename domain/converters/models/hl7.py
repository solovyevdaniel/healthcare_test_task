from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel



class MessageType(str, Enum):
    ADT_A01 = "ADT_A01"

    UNKNOWN = "unknown"

    def _missing_(cls, value):
        return cls.UNKNOWN

class EventType(str, Enum):
    A01 = "A01"

    UNKNOWN = "unknown"

    def _missing_(cls, value):
        return cls.UNKNOWN


class Address(BaseModel):
    line: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None


class Hl7HeaderSegment(BaseModel):
    """
    MSH Segment
    Purpose:Contains information about the message itself,
    such as sending and receiving applications, message type, and date/time.
    """
    sending_application: str | None = None
    sending_facility: str | None = None
    receiving_application: str | None = None
    receiving_facility: str | None = None
    created_at: datetime | None = None  # YYYYMMDDHHMMSS
    type: MessageType | None = None
    control_id: str | None = None
    processing_id: str | None = None
    version_id: str | None = None
    security: str | None = None
    acknowledgment_type: str | None = None
    application_acknowledgment_type: str | None = None


class Hl7EventSegment(BaseModel):
    """
    EVN Segment
    Purpose: Indicates the type of event that is being communicated in the message.
    """
    type: EventType | None = None
    created_at: datetime | None = None  # YYYYMMDDHHMMSS
    modified_at: datetime | None = None
    operation_id: str | None = None
    reason: str | None = None

class HL7PatientIdentificationSegment(BaseModel):
    """
    PID Segment
    Purpose: Contains demographic information about the patient.
    """
    set_id: int | None = None
    patient_id: int | None = None
    name: str | None = None
    birthdate: datetime | None = None  # YYYYMMDD
    sex: Literal["M", "F"] | None = None  # Male, Female
    address: Address | None = None
    phone: str | None = None
    email: str | None = None


class HL7PatientVisitSegment(BaseModel):
    """
    PV1
    Purpose: Contains information about a patient's visit to a healthcare facility.
    """
    set_id: int | None = None
    patient_class: str | None = None


class HL7Message(BaseModel):
    header: Hl7HeaderSegment | None = None
    event: Hl7EventSegment | None = None
    patient: HL7PatientIdentificationSegment | None = None
    visit: HL7PatientVisitSegment | None = None
