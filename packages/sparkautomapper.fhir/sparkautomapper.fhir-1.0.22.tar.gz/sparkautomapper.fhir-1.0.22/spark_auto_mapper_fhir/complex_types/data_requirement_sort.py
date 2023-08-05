from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING, Union

from pyspark.sql.types import StructType, DataType
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString

from spark_auto_mapper_fhir.extensions.custom.nested_extension_item import (
    NestedExtensionItem,
)

from spark_auto_mapper_fhir.base_types.fhir_complex_type_base import FhirComplexTypeBase
from spark_fhir_schemas.r4.complex_types.datarequirement_sort import (
    DataRequirement_SortSchema,
)


if TYPE_CHECKING:
    pass
    # id_ (string)
    # extension (Extension)
    # path (string)
    # direction (SortDirection)
    from spark_auto_mapper_fhir.value_sets.sort_direction import SortDirectionCode


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class DataRequirementSort(FhirComplexTypeBase):
    """
    DataRequirement.Sort
    fhir-base.xsd
        Describes a required data item for evaluation in terms of the type of data, and optional code or date-based filters of the data.
        If the element is present, it must have a value for at least one of the defined elements, an @id referenced from the Narrative, or extensions
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        use_date_for: Optional[List[str]] = None,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[NestedExtensionItem]] = None,
        path: FhirString,
        direction: SortDirectionCode,
    ) -> None:
        """
            Describes a required data item for evaluation in terms of the type of data,
        and optional code or date-based filters of the data.
            If the element is present, it must have a value for at least one of the
        defined elements, an @id referenced from the Narrative, or extensions

            :param id_: None
            :param extension: May be used to represent additional information that is not part of the basic
        definition of the element. To make the use of extensions safe and manageable,
        there is a strict set of governance  applied to the definition and use of
        extensions. Though any implementer can define an extension, there is a set of
        requirements that SHALL be met as part of the definition of the extension.
            :param path: The attribute of the sort. The specified path must be resolvable from the type
        of the required data. The path is allowed to contain qualifiers (.) to
        traverse sub-elements, as well as indexers ([x]) to traverse multiple-
        cardinality sub-elements. Note that the index must be an integer constant.
            :param direction: The direction of the sort, ascending or descending.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            path=path,
            direction=direction,
        )
        self.use_date_for = use_date_for

    def get_schema(
        self, include_extension: bool, extension_fields: Optional[List[str]] = None
    ) -> Optional[Union[StructType, DataType]]:
        return DataRequirement_SortSchema.get_schema(
            include_extension=include_extension,
            extension_fields=extension_fields,
            use_date_for=self.use_date_for,
        )
