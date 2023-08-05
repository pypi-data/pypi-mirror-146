from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString
from spark_auto_mapper_fhir.extensions.extension_base import ExtensionBase
from spark_auto_mapper_fhir.resources.resource import Resource

from spark_auto_mapper_fhir.base_types.fhir_backbone_element_base import (
    FhirBackboneElementBase,
)

if TYPE_CHECKING:
    pass
    # id_ (string)
    # extension (Extension)
    # modifierExtension (Extension)
    # code (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # End Import for References for code
    # Import for CodeableConcept for code
    from spark_auto_mapper_fhir.value_sets.manifestation_and_symptom_codes import (
        ManifestationAndSymptomCodesCode,
    )

    # End Import for CodeableConcept for code
    # detail (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for detail


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class DetectedIssueEvidence(FhirBackboneElementBase):
    """
    DetectedIssue.Evidence
        Indicates an actual or potential clinical issue with or between one or more active or proposed clinical actions for a patient; e.g. Drug-drug interaction, Ineffective treatment frequency, Procedure-condition conflict, etc.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        code: Optional[
            FhirList[CodeableConcept[ManifestationAndSymptomCodesCode]]
        ] = None,
        detail: Optional[FhirList[Reference[Resource]]] = None,
    ) -> None:
        """
            Indicates an actual or potential clinical issue with or between one or more
        active or proposed clinical actions for a patient; e.g. Drug-drug interaction,
        Ineffective treatment frequency, Procedure-condition conflict, etc.

            :param id_: None
            :param extension: May be used to represent additional information that is not part of the basic
        definition of the element. To make the use of extensions safe and manageable,
        there is a strict set of governance  applied to the definition and use of
        extensions. Though any implementer can define an extension, there is a set of
        requirements that SHALL be met as part of the definition of the extension.
            :param modifierExtension: May be used to represent additional information that is not part of the basic
        definition of the element and that modifies the understanding of the element
        in which it is contained and/or the understanding of the containing element's
        descendants. Usually modifier elements provide negation or qualification. To
        make the use of extensions safe and manageable, there is a strict set of
        governance applied to the definition and use of extensions. Though any
        implementer can define an extension, there is a set of requirements that SHALL
        be met as part of the definition of the extension. Applications processing a
        resource are required to check for modifier extensions.

        Modifier extensions SHALL NOT change the meaning of any elements on Resource
        or DomainResource (including cannot change the meaning of modifierExtension
        itself).
            :param code: A manifestation that led to the recording of this detected issue.
            :param detail: Links to resources that constitute evidence for the detected issue such as a
        GuidanceResponse or MeasureReport.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            code=code,
            detail=detail,
        )
