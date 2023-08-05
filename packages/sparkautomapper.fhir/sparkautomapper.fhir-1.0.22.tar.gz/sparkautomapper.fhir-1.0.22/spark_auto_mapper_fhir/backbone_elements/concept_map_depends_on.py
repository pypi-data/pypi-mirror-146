from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.fhir_types.string import FhirString
from spark_auto_mapper_fhir.extensions.extension_base import ExtensionBase
from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.base_types.fhir_backbone_element_base import (
    FhirBackboneElementBase,
)

if TYPE_CHECKING:
    pass
    # id_ (string)
    # extension (Extension)
    # modifierExtension (Extension)
    # property (uri)
    # system (canonical)
    from spark_auto_mapper_fhir.fhir_types.canonical import FhirCanonical

    # value (string)
    # display (string)


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class ConceptMapDependsOn(FhirBackboneElementBase):
    """
    ConceptMap.DependsOn
        A statement of relationships from one set of concepts to one or more other concepts - either concepts in code systems, or data element/data element concepts, or classes in class models.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        property: FhirUri,
        system: Optional[FhirCanonical] = None,
        value: FhirString,
        display: Optional[FhirString] = None,
    ) -> None:
        """
            A statement of relationships from one set of concepts to one or more other
        concepts - either concepts in code systems, or data element/data element
        concepts, or classes in class models.

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
            :param property: A reference to an element that holds a coded value that corresponds to a code
        system property. The idea is that the information model carries an element
        somewhere that is labeled to correspond with a code system property.
            :param system: An absolute URI that identifies the code system of the dependency code (if the
        source/dependency is a value set that crosses code systems).
            :param value: Identity (code or path) or the element/item/ValueSet/text that the map depends
        on / refers to.
            :param display: The display for the code. The display is only provided to help editors when
        editing the concept map.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            property=property,
            system=system,
            value=value,
            display=display,
        )
