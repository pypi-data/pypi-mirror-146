from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING, Union

from pyspark.sql.types import StructType, DataType
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString
from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.extensions.custom.nested_extension_item import (
    NestedExtensionItem,
)

from spark_auto_mapper_fhir.base_types.fhir_complex_type_base import FhirComplexTypeBase
from spark_fhir_schemas.r4.complex_types.identifier import IdentifierSchema


if TYPE_CHECKING:
    pass
    # id_ (string)
    # extension (Extension)
    # use (IdentifierUse)
    from spark_auto_mapper_fhir.value_sets.identifier_use import IdentifierUseCode

    # type_ (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # Import for CodeableConcept for type_
    from spark_auto_mapper_fhir.value_sets.identifier_type_codes import (
        IdentifierTypeCodesCode,
    )

    # End Import for CodeableConcept for type_
    # system (uri)
    # value (string)
    # period (Period)
    from spark_auto_mapper_fhir.complex_types.period import Period

    # assigner (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for assigner
    from spark_auto_mapper_fhir.resources.organization import Organization


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class Identifier(FhirComplexTypeBase):
    """
    Identifier
    fhir-base.xsd
        An identifier - identifies some entity uniquely and unambiguously. Typically this is used for business identifiers.
        If the element is present, it must have a value for at least one of the defined elements, an @id referenced from the Narrative, or extensions
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        use_date_for: Optional[List[str]] = None,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[NestedExtensionItem]] = None,
        use: Optional[IdentifierUseCode] = None,
        type_: Optional[CodeableConcept[IdentifierTypeCodesCode]] = None,
        system: Optional[FhirUri] = None,
        value: Optional[FhirString] = None,
        period: Optional[Period] = None,
        assigner: Optional[Reference[Organization]] = None,
    ) -> None:
        """
            An identifier - identifies some entity uniquely and unambiguously. Typically
        this is used for business identifiers.
            If the element is present, it must have a value for at least one of the
        defined elements, an @id referenced from the Narrative, or extensions

            :param id_: None
            :param extension: May be used to represent additional information that is not part of the basic
        definition of the element. To make the use of extensions safe and manageable,
        there is a strict set of governance  applied to the definition and use of
        extensions. Though any implementer can define an extension, there is a set of
        requirements that SHALL be met as part of the definition of the extension.
            :param use: The purpose of this identifier.
            :param type_: A coded type for the identifier that can be used to determine which identifier
        to use for a specific purpose.
            :param system: Establishes the namespace for the value - that is, a URL that describes a set
        values that are unique.
            :param value: The portion of the identifier typically relevant to the user and which is
        unique within the context of the system.
            :param period: Time period during which identifier is/was valid for use.
            :param assigner: Organization that issued/manages the identifier.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            use=use,
            type_=type_,
            system=system,
            value=value,
            period=period,
            assigner=assigner,
        )
        self.use_date_for = use_date_for

    def get_schema(
        self, include_extension: bool, extension_fields: Optional[List[str]] = None
    ) -> Optional[Union[StructType, DataType]]:
        return IdentifierSchema.get_schema(
            include_extension=include_extension,
            extension_fields=extension_fields,
            use_date_for=self.use_date_for,
        )
