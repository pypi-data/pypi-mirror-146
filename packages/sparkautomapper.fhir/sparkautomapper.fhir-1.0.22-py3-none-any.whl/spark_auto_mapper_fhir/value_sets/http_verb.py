from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class HTTPVerbCode(GenericTypeCode):
    """
    HTTPVerb
    From: http://hl7.org/fhir/http-verb in valuesets.xml
        HTTP verbs (in the HTTP command line). See [HTTP
    rfc](https://tools.ietf.org/html/rfc7231) for details.
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    http://hl7.org/fhir/http-verb
    """
    codeset: FhirUri = "http://hl7.org/fhir/http-verb"


class HTTPVerbCodeValues:
    """
    HTTP GET Command.
    From: http://hl7.org/fhir/http-verb in valuesets.xml
    """

    GET = HTTPVerbCode("GET")
    """
    HTTP HEAD Command.
    From: http://hl7.org/fhir/http-verb in valuesets.xml
    """
    HEAD = HTTPVerbCode("HEAD")
    """
    HTTP POST Command.
    From: http://hl7.org/fhir/http-verb in valuesets.xml
    """
    POST = HTTPVerbCode("POST")
    """
    HTTP PUT Command.
    From: http://hl7.org/fhir/http-verb in valuesets.xml
    """
    PUT = HTTPVerbCode("PUT")
    """
    HTTP DELETE Command.
    From: http://hl7.org/fhir/http-verb in valuesets.xml
    """
    DELETE = HTTPVerbCode("DELETE")
    """
    HTTP PATCH Command.
    From: http://hl7.org/fhir/http-verb in valuesets.xml
    """
    PATCH = HTTPVerbCode("PATCH")
