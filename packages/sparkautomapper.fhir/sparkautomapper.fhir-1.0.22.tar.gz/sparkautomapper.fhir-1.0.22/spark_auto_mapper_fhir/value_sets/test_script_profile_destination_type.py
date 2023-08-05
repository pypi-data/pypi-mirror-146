from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class TestScriptProfileDestinationTypeCode(GenericTypeCode):
    """
    TestScriptProfileDestinationType
    From: http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types in valuesets.xml
        This value set defines a set of codes that are used to indicate the profile
    type of a test system when acting as the destination within a TestScript.
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types
    """
    codeset: FhirUri = (
        "http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types"
    )


class TestScriptProfileDestinationTypeCodeValues:
    """
    General FHIR server used to respond to operations sent from a FHIR client.
    From: http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types in valuesets.xml
    """

    FHIRServer = TestScriptProfileDestinationTypeCode("FHIR-Server")
    """
    A FHIR server acting as a Structured Data Capture Form Manager.
    From: http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types in valuesets.xml
    """
    FHIRSDCFormManager = TestScriptProfileDestinationTypeCode("FHIR-SDC-FormManager")
    """
    A FHIR server acting as a Structured Data Capture Form Processor.
    From: http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types in valuesets.xml
    """
    FHIRSDCFormProcessor = TestScriptProfileDestinationTypeCode(
        "FHIR-SDC-FormProcessor"
    )
    """
    A FHIR server acting as a Structured Data Capture Form Receiver.
    From: http://terminology.hl7.org/CodeSystem/testscript-profile-destination-types in valuesets.xml
    """
    FHIRSDCFormReceiver = TestScriptProfileDestinationTypeCode("FHIR-SDC-FormReceiver")
