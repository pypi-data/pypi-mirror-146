from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class Iso3166_1_NCode(GenericTypeCode):
    """
    Iso3166-1-N
    From: http://hl7.org/fhir/ValueSet/iso3166-1-N in valuesets.xml
        This value set defines the ISO 3166 Part 1 Numeric codes
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    urn:iso:std:iso:3166
    """
    codeset: FhirUri = "urn:iso:std:iso:3166"
