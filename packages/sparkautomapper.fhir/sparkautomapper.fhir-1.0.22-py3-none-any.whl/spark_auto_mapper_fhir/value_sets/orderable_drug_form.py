from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class OrderableDrugForm(GenericTypeCode):
    """
    v3.orderableDrugForm
    From: http://terminology.hl7.org/ValueSet/v3-orderableDrugForm in v3-codesystems.xml
          OpenIssue:
    Missing description.
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm
    """
    codeset: FhirUri = "http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm"


class OrderableDrugFormValues:
    """
    AdministrableDrugForm
    From: http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm in v3-codesystems.xml
    """

    AdministrableDrugForm = OrderableDrugForm("_AdministrableDrugForm")
    """
    DispensableDrugForm
    From: http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm in v3-codesystems.xml
    """
    DispensableDrugForm = OrderableDrugForm("_DispensableDrugForm")
