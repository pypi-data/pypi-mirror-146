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
    # reference (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for reference
    # code (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # End Import for References for code
    # Import for CodeableConcept for code
    from spark_auto_mapper_fhir.value_sets.contract_resource_asset_context_codes import (
        ContractResourceAssetContextCodesCode,
    )

    # End Import for CodeableConcept for code
    # text (string)


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class ContractContext(FhirBackboneElementBase):
    """
    Contract.Context
        Legally enforceable, formally recorded unilateral or bilateral directive i.e., a policy or agreement.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        reference: Optional[Reference[Resource]] = None,
        code: Optional[
            FhirList[CodeableConcept[ContractResourceAssetContextCodesCode]]
        ] = None,
        text: Optional[FhirString] = None,
    ) -> None:
        """
            Legally enforceable, formally recorded unilateral or bilateral directive i.e.,
        a policy or agreement.

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
            :param reference: Asset context reference may include the creator, custodian, or owning Person
        or Organization (e.g., bank, repository),  location held, e.g., building,
        jurisdiction.
            :param code: Coded representation of the context generally or of the Referenced entity,
        such as the asset holder type or location.
            :param text: Context description.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            reference=reference,
            code=code,
            text=text,
        )
