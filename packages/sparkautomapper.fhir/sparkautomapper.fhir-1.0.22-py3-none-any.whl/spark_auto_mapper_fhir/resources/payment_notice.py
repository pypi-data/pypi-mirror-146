from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING, Union

# noinspection PyPackageRequirements
from pyspark.sql.types import StructType, DataType
from spark_auto_mapper_fhir.fhir_types.date import FhirDate
from spark_auto_mapper_fhir.fhir_types.date_time import FhirDateTime
from spark_auto_mapper_fhir.fhir_types.list import FhirList
from spark_auto_mapper_fhir.complex_types.meta import Meta
from spark_auto_mapper_fhir.extensions.extension_base import ExtensionBase
from spark_auto_mapper_fhir.fhir_types.id import FhirId
from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.base_types.fhir_resource_base import FhirResourceBase
from spark_fhir_schemas.r4.resources.paymentnotice import PaymentNoticeSchema

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

    # status (FinancialResourceStatusCodes)
    from spark_auto_mapper_fhir.value_sets.financial_resource_status_codes import (
        FinancialResourceStatusCodesCode,
    )

    # request (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for request
    from spark_auto_mapper_fhir.resources.resource import Resource

    # response (Reference)
    # Imports for References for response
    # created (dateTime)
    # provider (Reference)
    # Imports for References for provider
    from spark_auto_mapper_fhir.resources.practitioner import Practitioner
    from spark_auto_mapper_fhir.resources.practitioner_role import PractitionerRole
    from spark_auto_mapper_fhir.resources.organization import Organization

    # payment (Reference)
    # Imports for References for payment
    from spark_auto_mapper_fhir.resources.payment_reconciliation import (
        PaymentReconciliation,
    )

    # paymentDate (date)
    # payee (Reference)
    # Imports for References for payee
    # recipient (Reference)
    # Imports for References for recipient
    # amount (Money)
    from spark_auto_mapper_fhir.complex_types.money import Money

    # paymentStatus (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # Import for CodeableConcept for paymentStatus
    from spark_auto_mapper_fhir.value_sets.payment_status_codes import (
        PaymentStatusCodesCode,
    )

    # End Import for CodeableConcept for paymentStatus


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class PaymentNotice(FhirResourceBase):
    """
    PaymentNotice
    paymentnotice.xsd
        This resource provides the status of the payment for goods and services
    rendered, and the request and response resource references.
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
        status: FinancialResourceStatusCodesCode,
        request: Optional[Reference[Resource]] = None,
        response: Optional[Reference[Resource]] = None,
        created: FhirDateTime,
        provider: Optional[
            Reference[Union[Practitioner, PractitionerRole, Organization]]
        ] = None,
        payment: Reference[PaymentReconciliation],
        paymentDate: Optional[FhirDate] = None,
        payee: Optional[
            Reference[Union[Practitioner, PractitionerRole, Organization]]
        ] = None,
        recipient: Reference[Organization],
        amount: Money,
        paymentStatus: Optional[CodeableConcept[PaymentStatusCodesCode]] = None,
    ) -> None:
        """
            This resource provides the status of the payment for goods and services
        rendered, and the request and response resource references.
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
            :param identifier: A unique identifier assigned to this payment notice.
            :param status: The status of the resource instance.
            :param request: Reference of resource for which payment is being made.
            :param response: Reference of response to resource for which payment is being made.
            :param created: The date when this resource was created.
            :param provider: The practitioner who is responsible for the services rendered to the patient.
            :param payment: A reference to the payment which is the subject of this notice.
            :param paymentDate: The date when the above payment action occurred.
            :param payee: The party who will receive or has received payment that is the subject of this
        notification.
            :param recipient: The party who is notified of the payment status.
            :param amount: The amount sent to the payee.
            :param paymentStatus: A code indicating whether payment has been sent or cleared.
        """
        super().__init__(
            resourceType="PaymentNotice",
            id_=id_,
            meta=meta,
            implicitRules=implicitRules,
            language=language,
            text=text,
            contained=contained,
            extension=extension,
            modifierExtension=modifierExtension,
            identifier=identifier,
            status=status,
            request=request,
            response=response,
            created=created,
            provider=provider,
            payment=payment,
            paymentDate=paymentDate,
            payee=payee,
            recipient=recipient,
            amount=amount,
            paymentStatus=paymentStatus,
        )

        self.use_date_for = use_date_for

    def get_schema(
        self, include_extension: bool, extension_fields: Optional[List[str]] = None
    ) -> Optional[Union[StructType, DataType]]:
        return PaymentNoticeSchema.get_schema(
            include_extension=include_extension,
            extension_fields=extension_fields,
            use_date_for=self.use_date_for,
        )
