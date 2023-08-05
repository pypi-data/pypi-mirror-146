from __future__ import annotations
from typing import Optional, TYPE_CHECKING

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
    # substance (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # End Import for References for substance
    # Import for CodeableConcept for substance
    from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode

    # End Import for CodeableConcept for substance
    # strength (Ratio)
    from spark_auto_mapper_fhir.complex_types.ratio import Ratio

    # strengthLowLimit (Ratio)
    # measurementPoint (string)
    # country (CodeableConcept)
    # End Import for References for country
    # Import for CodeableConcept for country
    # End Import for CodeableConcept for country


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class MedicinalProductIngredientReferenceStrength(FhirBackboneElementBase):
    """
    MedicinalProductIngredient.ReferenceStrength
        An ingredient of a manufactured item or pharmaceutical product.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        substance: Optional[CodeableConcept[GenericTypeCode]] = None,
        strength: Ratio,
        strengthLowLimit: Optional[Ratio] = None,
        measurementPoint: Optional[FhirString] = None,
        country: Optional[FhirList[CodeableConcept[GenericTypeCode]]] = None,
    ) -> None:
        """
            An ingredient of a manufactured item or pharmaceutical product.

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
            :param substance: Relevant reference substance.
            :param strength: Strength expressed in terms of a reference substance.
            :param strengthLowLimit: Strength expressed in terms of a reference substance.
            :param measurementPoint: For when strength is measured at a particular point or distance.
            :param country: The country or countries for which the strength range applies.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            substance=substance,
            strength=strength,
            strengthLowLimit=strengthLowLimit,
            measurementPoint=measurementPoint,
            country=country,
        )
