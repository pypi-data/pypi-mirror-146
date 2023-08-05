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
    # attachment (Attachment)
    from spark_auto_mapper_fhir.complex_types.attachment import Attachment

    # format (Coding)
    from spark_auto_mapper_fhir.complex_types.coding import Coding

    # End Import for References for format
    # Import for CodeableConcept for format
    from spark_auto_mapper_fhir.value_sets.document_reference_format_code_set import (
        DocumentReferenceFormatCodeSetCode,
    )

    # End Import for CodeableConcept for format


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class DocumentReferenceContent(FhirBackboneElementBase):
    """
    DocumentReference.Content
        A reference to a document of any kind for any purpose. Provides metadata about the document so that the document can be discovered and managed. The scope of a document is any seralized object with a mime-type, so includes formal patient centric documents (CDA), cliical notes, scanned paper, and non-patient specific documents like policy text.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        attachment: Attachment,
        format: Optional[Coding[DocumentReferenceFormatCodeSetCode]] = None,
    ) -> None:
        """
            A reference to a document of any kind for any purpose. Provides metadata about
        the document so that the document can be discovered and managed. The scope of
        a document is any seralized object with a mime-type, so includes formal
        patient centric documents (CDA), cliical notes, scanned paper, and non-patient
        specific documents like policy text.

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
            :param attachment: The document or URL of the document along with critical metadata to prove
        content has integrity.
            :param format: An identifier of the document encoding, structure, and template that the
        document conforms to beyond the base format indicated in the mimeType.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            attachment=attachment,
            format=format,
        )
