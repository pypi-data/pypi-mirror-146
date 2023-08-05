from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Union

from spark_auto_mapper_fhir.fhir_types.boolean import FhirBoolean
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
    # type_ (CodeableConcept)
    from spark_auto_mapper_fhir.complex_types.codeable_concept import CodeableConcept

    # End Import for References for type_
    # Import for CodeableConcept for type_
    from spark_auto_mapper_fhir.value_sets.participation_role_type import (
        ParticipationRoleTypeCode,
    )

    # End Import for CodeableConcept for type_
    # role (CodeableConcept)
    # End Import for References for role
    # Import for CodeableConcept for role
    from spark_auto_mapper_fhir.value_sets.security_role_type import (
        SecurityRoleTypeCode,
    )

    # End Import for CodeableConcept for role
    # who (Reference)
    from spark_auto_mapper_fhir.complex_types.reference import Reference

    # Imports for References for who
    from spark_auto_mapper_fhir.resources.practitioner_role import PractitionerRole
    from spark_auto_mapper_fhir.resources.practitioner import Practitioner
    from spark_auto_mapper_fhir.resources.organization import Organization
    from spark_auto_mapper_fhir.resources.device import Device
    from spark_auto_mapper_fhir.resources.patient import Patient
    from spark_auto_mapper_fhir.resources.related_person import RelatedPerson

    # altId (string)
    # name (string)
    # requestor (boolean)
    # location (Reference)
    # Imports for References for location
    from spark_auto_mapper_fhir.resources.location import Location

    # policy (uri)
    # media (Coding)
    from spark_auto_mapper_fhir.complex_types.coding import Coding

    # End Import for References for media
    # Import for CodeableConcept for media
    from spark_auto_mapper_fhir.value_sets.media_type_code import MediaTypeCodeCode

    # End Import for CodeableConcept for media
    # network (AuditEvent.Network)
    from spark_auto_mapper_fhir.backbone_elements.audit_event_network import (
        AuditEventNetwork,
    )

    # purposeOfUse (CodeableConcept)
    # End Import for References for purposeOfUse
    # Import for CodeableConcept for purposeOfUse
    from spark_auto_mapper_fhir.value_sets.purpose_of_use import PurposeOfUse

    # End Import for CodeableConcept for purposeOfUse


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class AuditEventAgent(FhirBackboneElementBase):
    """
    AuditEvent.Agent
        A record of an event made for purposes of maintaining a security log. Typical uses include detection of intrusion attempts and monitoring for inappropriate usage.
    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        *,
        id_: Optional[FhirString] = None,
        extension: Optional[FhirList[ExtensionBase]] = None,
        modifierExtension: Optional[FhirList[ExtensionBase]] = None,
        type_: Optional[CodeableConcept[ParticipationRoleTypeCode]] = None,
        role: Optional[FhirList[CodeableConcept[SecurityRoleTypeCode]]] = None,
        who: Optional[
            Reference[
                Union[
                    PractitionerRole,
                    Practitioner,
                    Organization,
                    Device,
                    Patient,
                    RelatedPerson,
                ]
            ]
        ] = None,
        altId: Optional[FhirString] = None,
        name: Optional[FhirString] = None,
        requestor: FhirBoolean,
        location: Optional[Reference[Location]] = None,
        policy: Optional[FhirList[FhirUri]] = None,
        media: Optional[Coding[MediaTypeCodeCode]] = None,
        network: Optional[AuditEventNetwork] = None,
        purposeOfUse: Optional[FhirList[CodeableConcept[PurposeOfUse]]] = None,
    ) -> None:
        """
            A record of an event made for purposes of maintaining a security log. Typical
        uses include detection of intrusion attempts and monitoring for inappropriate
        usage.

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
            :param type_: Specification of the participation type the user plays when performing the
        event.
            :param role: The security role that the user was acting under, that come from local codes
        defined by the access control security system (e.g. RBAC, ABAC) used in the
        local context.
            :param who: Reference to who this agent is that was involved in the event.
            :param altId: Alternative agent Identifier. For a human, this should be a user identifier
        text string from authentication system. This identifier would be one known to
        a common authentication system (e.g. single sign-on), if available.
            :param name: Human-meaningful name for the agent.
            :param requestor: Indicator that the user is or is not the requestor, or initiator, for the
        event being audited.
            :param location: Where the event occurred.
            :param policy: The policy or plan that authorized the activity being recorded. Typically, a
        single activity may have multiple applicable policies, such as patient
        consent, guarantor funding, etc. The policy would also indicate the security
        token used.
            :param media: Type of media involved. Used when the event is about exporting/importing onto
        media.
            :param network: Logical network location for application activity, if the activity has a
        network location.
            :param purposeOfUse: The reason (purpose of use), specific to this agent, that was used during the
        event being recorded.
        """
        super().__init__(
            id_=id_,
            extension=extension,
            modifierExtension=modifierExtension,
            type_=type_,
            role=role,
            who=who,
            altId=altId,
            name=name,
            requestor=requestor,
            location=location,
            policy=policy,
            media=media,
            network=network,
            purposeOfUse=purposeOfUse,
        )
