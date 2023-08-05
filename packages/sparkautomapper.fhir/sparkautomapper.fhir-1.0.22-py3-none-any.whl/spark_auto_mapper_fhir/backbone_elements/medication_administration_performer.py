from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Union

from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString
from spark_auto_mapper_fhir.extensions.extension_base import ExtensionBase

from spark_auto_mapper_fhir.base_types.fhir_backbone_element_base import (
    FhirBackboneElementBase,
)

if TYPE_CHECKING:
    pass
    # id_ (string)
    # extension (Extension)
    # modifierExtension (Extension)
    # function (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # End Import for References for function
    # Import for CodeableConcept for function
    from spark_auto_mapper_fhir.value_sets.medication_administration_performer_function_codes import (
        MedicationAdministrationPerformerFunctionCodesCode,
    )

    # End Import for CodeableConcept for function
    # actor (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for actor
    from spark_auto_mapper_fhir.resources.practitioner import Practitioner
    from spark_auto_mapper_fhir.resources.practitioner_role import PractitionerRole
    from spark_auto_mapper_fhir.resources.patient import Patient
    from spark_auto_mapper_fhir.resources.related_person import RelatedPerson
    from spark_auto_mapper_fhir.resources.device import Device


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class MedicationAdministrationPerformer(FhirBackboneElementBase):
    """
    MedicationAdministration.Performer
        Describes the event of a patient consuming or otherwise being administered a medication.  This may be as simple as swallowing a tablet or it may be a long running infusion.  Related resources tie this event to the authorizing prescription, and the specific encounter between patient and health care practitioner.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        function: Optional[
            CodeableConcept[MedicationAdministrationPerformerFunctionCodesCode]
        ] = None,
        actor: Reference[
            Union[Practitioner, PractitionerRole, Patient, RelatedPerson, Device]
        ],
    ) -> None:
        """
            Describes the event of a patient consuming or otherwise being administered a
        medication.  This may be as simple as swallowing a tablet or it may be a long
        running infusion.  Related resources tie this event to the authorizing
        prescription, and the specific encounter between patient and health care
        practitioner.

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
            :param function: Distinguishes the type of involvement of the performer in the medication
        administration.
            :param actor: Indicates who or what performed the medication administration.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            function=function,
            actor=actor,
        )
