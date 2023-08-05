from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class ContractResourcePartyRoleCodesCode(GenericTypeCode):
    """
    ContractResourcePartyRoleCodes
    From: http://hl7.org/fhir/contract-party-role in valuesets.xml
        This value set contract specific codes for offer party participation.
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    http://hl7.org/fhir/contract-party-role
    """
    codeset: FhirUri = "http://hl7.org/fhir/contract-party-role"


class ContractResourcePartyRoleCodesCodeValues:
    """
    To be completed
    From: http://hl7.org/fhir/contract-party-role in valuesets.xml
    """

    FLunky = ContractResourcePartyRoleCodesCode("flunky")
