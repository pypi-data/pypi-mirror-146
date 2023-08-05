from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING, Union

from pyspark.sql.types import StructType, DataType
from spark_auto_mapper_fhir.fhir_types.date_time import FhirDateTime
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString

from spark_auto_mapper_fhir.extensions.custom.nested_extension_item import (
    NestedExtensionItem,
)

from spark_auto_mapper_fhir.base_types.fhir_complex_type_base import FhirComplexTypeBase
from spark_fhir_schemas.r4.complex_types.attachment import AttachmentSchema


if TYPE_CHECKING:
    pass
    # id_ (string)
    # extension (Extension)
    # contentType (Mime Types)
    from spark_auto_mapper_fhir.value_sets.mime_types import MimeTypesCode

    # language (CommonLanguages)
    from spark_auto_mapper_fhir.value_sets.common_languages import CommonLanguagesCode

    # data (base64Binary)
    from spark_auto_mapper_fhir.fhir_types.base64_binary import FhirBase64Binary

    # url (url)
    from spark_auto_mapper_fhir.fhir_types.url import FhirUrl

    # size (unsignedInt)
    from spark_auto_mapper_fhir.fhir_types.unsigned_int import FhirUnsignedInt

    # hash (base64Binary)
    # title (string)
    # creation (dateTime)


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class Attachment(FhirComplexTypeBase):
    """
    Attachment
    fhir-base.xsd
        For referring to data content defined in other formats.
        If the element is present, it must have a value for at least one of the defined elements, an @id referenced from the Narrative, or extensions
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        use_date_for: Optional[List[str]] = None,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[NestedExtensionItem]] = None,
        contentType: Optional[MimeTypesCode] = None,
        language: Optional[CommonLanguagesCode] = None,
        data: Optional[FhirBase64Binary] = None,
        url: Optional[FhirUrl] = None,
        size: Optional[FhirUnsignedInt] = None,
        hash: Optional[FhirBase64Binary] = None,
        title: Optional[FhirString] = None,
        creation: Optional[FhirDateTime] = None,
    ) -> None:
        """
            For referring to data content defined in other formats.
            If the element is present, it must have a value for at least one of the
        defined elements, an @id referenced from the Narrative, or extensions

            :param id_: None
            :param extension: May be used to represent additional information that is not part of the basic
        definition of the element. To make the use of extensions safe and manageable,
        there is a strict set of governance  applied to the definition and use of
        extensions. Though any implementer can define an extension, there is a set of
        requirements that SHALL be met as part of the definition of the extension.
            :param contentType: Identifies the type of the data in the attachment and allows a method to be
        chosen to interpret or render the data. Includes mime type parameters such as
        charset where appropriate.
            :param language: The human language of the content. The value can be any valid value according
        to BCP 47.
            :param data: The actual data of the attachment - a sequence of bytes, base64 encoded.
            :param url: A location where the data can be accessed.
            :param size: The number of bytes of data that make up this attachment (before base64
        encoding, if that is done).
            :param hash: The calculated hash of the data using SHA-1. Represented using base64.
            :param title: A label or set of text to display in place of the data.
            :param creation: The date that the attachment was first created.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            contentType=contentType,
            language=language,
            data=data,
            url=url,
            size=size,
            hash=hash,
            title=title,
            creation=creation,
        )
        self.use_date_for = use_date_for

    def get_schema(
        self, include_extension: bool, extension_fields: Optional[List[str]] = None
    ) -> Optional[Union[StructType, DataType]]:
        return AttachmentSchema.get_schema(
            include_extension=include_extension,
            extension_fields=extension_fields,
            use_date_for=self.use_date_for,
        )
