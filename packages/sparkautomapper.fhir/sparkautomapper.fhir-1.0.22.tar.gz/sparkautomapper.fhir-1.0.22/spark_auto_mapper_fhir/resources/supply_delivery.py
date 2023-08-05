from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING, Union

# noinspection PyPackageRequirements
from pyspark.sql.types import StructType, DataType
from spark_auto_mapper_fhir.fhir_types.date_time import FhirDateTime
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.complex_types.meta import Meta
from spark_auto_mapper_fhir.extensions.extension_base import ExtensionBase
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.base_types.fhir_resource_base import FhirResourceBase
from spark_fhir_schemas.r4.resources.supplydelivery import SupplyDeliverySchema

if TYPE_CHECKING:
    pass
    # id_ (id)
    # meta (Meta)
    # implicitRules (uri)
    # language (CommonLanguages)
    from spark_auto_mapper_fhir.value_sets.common_languages import CommonLanguagesCode

    # text (Narrative)
    from spark_auto_mapper_fhir.complex_types.narrative import Narrative

    # contained (ResourceContainer)
    from spark_auto_mapper_fhir.complex_types.resource_container import (
        ResourceContainer,
    )

    # extension (Extension)
    # modifierExtension (Extension)
    # identifier (Identifier)
    from spark_auto_mapper_fhir.complex_types.identifier import Identifier

    # basedOn (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for basedOn
    from spark_auto_mapper_fhir.resources.supply_request import SupplyRequest

    # partOf (Reference)
    # Imports for References for partOf
    from spark_auto_mapper_fhir.resources.contract import Contract

    # status (SupplyDeliveryStatus)
    from spark_auto_mapper_fhir.value_sets.supply_delivery_status import (
        SupplyDeliveryStatusCode,
    )

    # patient (Reference)
    # Imports for References for patient
    from spark_auto_mapper_fhir.resources.patient import Patient

    # type_ (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # Import for CodeableConcept for type_
    from spark_auto_mapper_fhir.value_sets.supply_item_type import SupplyItemTypeCode

    # End Import for CodeableConcept for type_
    # suppliedItem (SupplyDelivery.SuppliedItem)
    from spark_auto_mapper_fhir.backbone_elements.supply_delivery_supplied_item import (
        SupplyDeliverySuppliedItem,
    )

    # occurrenceDateTime (dateTime)
    # occurrencePeriod (Period)
    from spark_auto_mapper_fhir.complex_types.period import Period

    # occurrenceTiming (Timing)
    from spark_auto_mapper_fhir.backbone_elements.timing import Timing

    # supplier (Reference)
    # Imports for References for supplier
    from spark_auto_mapper_fhir.resources.practitioner import Practitioner
    from spark_auto_mapper_fhir.resources.practitioner_role import PractitionerRole
    from spark_auto_mapper_fhir.resources.organization import Organization

    # destination (Reference)
    # Imports for References for destination
    from spark_auto_mapper_fhir.resources.location import Location

    # receiver (Reference)
    # Imports for References for receiver


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class SupplyDelivery(FhirResourceBase):
    """
    SupplyDelivery
    supplydelivery.xsd
        Record of delivery of what is supplied.
        If the element is present, it must have either a @value, an @id, or extensions
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        use_date_for: Optional[List[str]] = None,
        id_: Optional[FhirId] = None,
        meta: Optional[Meta] = None,
        implicitRules: Optional[FhirUri] = None,
        language: Optional[CommonLanguagesCode] = None,
        text: Optional[Narrative] = None,
        contained: Optional[FhirList[ResourceContainer]] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        identifier: Optional[FhirList[Identifier]] = None,
        basedOn: Optional[FhirList[Reference[SupplyRequest]]] = None,
        partOf: Optional[FhirList[Reference[Union[SupplyDelivery, Contract]]]] = None,
        status: Optional[SupplyDeliveryStatusCode] = None,
        patient: Optional[Reference[Patient]] = None,
        type_: Optional[CodeableConcept[SupplyItemTypeCode]] = None,
        suppliedItem: Optional[SupplyDeliverySuppliedItem] = None,
        occurrenceDateTime: Optional[FhirDateTime] = None,
        occurrencePeriod: Optional[Period] = None,
        occurrenceTiming: Optional[Timing] = None,
        supplier: Optional[
            Reference[Union[Practitioner, PractitionerRole, Organization]]
        ] = None,
        destination: Optional[Reference[Location]] = None,
        receiver: Optional[
            FhirList[Reference[Union[Practitioner, PractitionerRole]]]
        ] = None,
    ) -> None:
        """
            Record of delivery of what is supplied.
            If the element is present, it must have either a @value, an @id, or extensions

            :param id_: The logical id of the resource, as used in the URL for the resource. Once
        assigned, this value never changes.
            :param meta: The metadata about the resource. This is content that is maintained by the
        infrastructure. Changes to the content might not always be associated with
        version changes to the resource.
            :param implicitRules: A reference to a set of rules that were followed when the resource was
        constructed, and which must be understood when processing the content. Often,
        this is a reference to an implementation guide that defines the special rules
        along with other profiles etc.
            :param language: The base language in which the resource is written.
            :param text: A human-readable narrative that contains a summary of the resource and can be
        used to represent the content of the resource to a human. The narrative need
        not encode all the structured data, but is required to contain sufficient
        detail to make it "clinically safe" for a human to just read the narrative.
        Resource definitions may define what content should be represented in the
        narrative to ensure clinical safety.
            :param contained: These resources do not have an independent existence apart from the resource
        that contains them - they cannot be identified independently, and nor can they
        have their own independent transaction scope.
            :param extension: May be used to represent additional information that is not part of the basic
        definition of the resource. To make the use of extensions safe and manageable,
        there is a strict set of governance  applied to the definition and use of
        extensions. Though any implementer can define an extension, there is a set of
        requirements that SHALL be met as part of the definition of the extension.
            :param modifierExtension: May be used to represent additional information that is not part of the basic
        definition of the resource and that modifies the understanding of the element
        that contains it and/or the understanding of the containing element's
        descendants. Usually modifier elements provide negation or qualification. To
        make the use of extensions safe and manageable, there is a strict set of
        governance applied to the definition and use of extensions. Though any
        implementer is allowed to define an extension, there is a set of requirements
        that SHALL be met as part of the definition of the extension. Applications
        processing a resource are required to check for modifier extensions.

        Modifier extensions SHALL NOT change the meaning of any elements on Resource
        or DomainResource (including cannot change the meaning of modifierExtension
        itself).
            :param identifier: Identifier for the supply delivery event that is used to identify it across
        multiple disparate systems.
            :param basedOn: A plan, proposal or order that is fulfilled in whole or in part by this event.
            :param partOf: A larger event of which this particular event is a component or step.
            :param status: A code specifying the state of the dispense event.
            :param patient: A link to a resource representing the person whom the delivered item is for.
            :param type_: Indicates the type of dispensing event that is performed. Examples include:
        Trial Fill, Completion of Trial, Partial Fill, Emergency Fill, Samples, etc.
            :param suppliedItem: The item that is being delivered or has been supplied.
            :param occurrenceDateTime: None
            :param occurrencePeriod: None
            :param occurrenceTiming: None
            :param supplier: The individual responsible for dispensing the medication, supplier or device.
            :param destination: Identification of the facility/location where the Supply was shipped to, as
        part of the dispense event.
            :param receiver: Identifies the person who picked up the Supply.
        """
        super().__init__(
            resourceType="SupplyDelivery",
            id_=id_,
            meta=meta,
            implicitRules=implicitRules,
            language=language,
            text=text,
            contained=contained,
            extension=extension,
            modifierExtension=modifierExtension,
            identifier=identifier,
            basedOn=basedOn,
            partOf=partOf,
            status=status,
            patient=patient,
            type_=type_,
            suppliedItem=suppliedItem,
            occurrenceDateTime=occurrenceDateTime,
            occurrencePeriod=occurrencePeriod,
            occurrenceTiming=occurrenceTiming,
            supplier=supplier,
            destination=destination,
            receiver=receiver,
        )

        self.use_date_for = use_date_for

    def get_schema(
        self, include_extension: bool, extension_fields: Optional[List[str]] = None
    ) -> Optional[Union[StructType, DataType]]:
        return SupplyDeliverySchema.get_schema(
            include_extension=include_extension,
            extension_fields=extension_fields,
            use_date_for=self.use_date_for,
        )
