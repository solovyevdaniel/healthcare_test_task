from .base import BaseMessageConverter
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter
from fhir.resources.humanname import HumanName
from fhir.resources.address import Address
from fhir.resources.contactpoint import ContactPoint

from .models.fhir import FhirMessage
from .models.hl7 import HL7Message


class Hl7Ad01ToFHIRConverter(BaseMessageConverter):
    def convert(self, message: HL7Message) -> FhirMessage:
        patient = Patient(
            id=message.patient.patient_id,
            name=[HumanName(family=message.patient.name, given=[message.patient.name])],
            gender="male" if message.patient.sex == "M" else "female",
            birthDate=message.patient.birthdate,
            address=[Address(
                line=[message.patient.address.line],
                city=message.patient.address.city,
                state=message.patient.address.state,
                postalCode=message.patient.address.postal_code
            )],
            telecom=[
                ContactPoint(system="phone", value=message.patient.phone),
                ContactPoint(system="email", value=message.patient.email)
            ]
        )

        encounter = Encounter(
            id=message.header.control_id,
            status="in-progress",
            subject={"reference": f"Patient/{patient.id}"},
        )
        return FhirMessage(patient=patient, encounter=encounter)
