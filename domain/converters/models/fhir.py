from pydantic.v1 import BaseModel
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter


class FhirMessage(BaseModel):
    patient: Patient | None = None
    encounter: Encounter | None = None
