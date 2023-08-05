from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class SubstanceAdminSubstitutionReason(GenericTypeCode):
    """
    v3.SubstanceAdminSubstitutionReason
    From: http://terminology.hl7.org/ValueSet/v3-SubstanceAdminSubstitutionReason in v3-codesystems.xml
        No Description Provided
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    http://terminology.hl7.org/CodeSystem/v3-ActReason
    """
    codeset: FhirUri = "http://terminology.hl7.org/CodeSystem/v3-ActReason"


class SubstanceAdminSubstitutionReasonValues:
    """
    Identifies the reason the patient is assigned to this accommodation type
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """

    ActAccommodationReason = SubstanceAdminSubstitutionReason("_ActAccommodationReason")
    """
    Description:Codes used to specify reasons or criteria relating to coverage
    provided under a policy or program.  May be used to convey reasons pertaining
    to coverage contractual provisions, including criteria for eligibility,
    coverage limitations, coverage maximums, or financial participation required
    of covered parties.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActCoverageReason = SubstanceAdminSubstitutionReason("_ActCoverageReason")
    """
    Description:The rationale or purpose for an act relating to information
    management, such as archiving information for the purpose of complying with an
    enterprise data retention policy.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActInformationManagementReason = SubstanceAdminSubstitutionReason(
        "_ActInformationManagementReason"
    )
    """
    Description: Types of reasons why a substance is invalid for use.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActInvalidReason = SubstanceAdminSubstitutionReason("_ActInvalidReason")
    """
    Domain specifies the codes used to describe reasons why a Provider is
    cancelling an Invoice or Invoice Grouping.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActInvoiceCancelReason = SubstanceAdminSubstitutionReason("_ActInvoiceCancelReason")
    """
    A coded description of the reason for why a patient did not receive a
    scheduled immunization.
    
                            (important for public health strategy
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActNoImmunizationReason = SubstanceAdminSubstitutionReason(
        "_ActNoImmunizationReason"
    )
    """
    Indicates why a fulfiller refused to fulfill a supply order, and considered it
    important to notify other providers of their decision.  E.g. "Suspect fraud",
    "Possible abuse", "Contraindicated".
    
                            (used when capturing 'refusal to fill' annotations)
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActSupplyFulfillmentRefusalReason = SubstanceAdminSubstitutionReason(
        "_ActSupplyFulfillmentRefusalReason"
    )
    """
    Definition:Specifies the reason that an event occurred in a clinical research
    study.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ClinicalResearchEventReason = SubstanceAdminSubstitutionReason(
        "_ClinicalResearchEventReason"
    )
    """
    Definition:SSpecifies the reason that a test was performed or observation
    collected in a clinical research study.
    
    
                               Note:This set of codes are not strictly reasons,
    but are used in the currently Normative standard.  Future revisions of the
    specification will model these as ActRelationships and thes codes may
    subsequently be retired.  Thus, these codes should not be used for new
    specifications.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ClinicalResearchObservationReason = SubstanceAdminSubstitutionReason(
        "_ClinicalResearchObservationReason"
    )
    """
    Description:Indicates why the prescription should be suspended.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    CombinedPharmacyOrderSuspendReasonCode = SubstanceAdminSubstitutionReason(
        "_CombinedPharmacyOrderSuspendReasonCode"
    )
    """
    Description:Identifies reasons for nullifying (retracting) a particular
    control act.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ControlActNullificationReasonCode = SubstanceAdminSubstitutionReason(
        "_ControlActNullificationReasonCode"
    )
    """
    Description: Reasons to refuse a transaction to be undone.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ControlActNullificationRefusalReasonType = SubstanceAdminSubstitutionReason(
        "_ControlActNullificationRefusalReasonType"
    )
    """
    Identifies why a specific query, request, or other trigger event occurred.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ControlActReason = SubstanceAdminSubstitutionReason("_ControlActReason")
    """
    Description:Identifies why a change is being made to a  record.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    GenericUpdateReasonCode = SubstanceAdminSubstitutionReason(
        "_GenericUpdateReasonCode"
    )
    """
    Definition:A collection of concepts identifying why the patient's profile is
    being queried.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    PatientProfileQueryReason = SubstanceAdminSubstitutionReason(
        "_PatientProfileQueryReasonCode"
    )
    """
    Definition:Indicates why the request to transfer a prescription from one
    dispensing facility to another has been refused.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    PharmacySupplyRequestFulfillerRevisionRefusalReasonCode = (
        SubstanceAdminSubstitutionReason(
            "_PharmacySupplyRequestFulfillerRevisionRefusalReasonCode"
        )
    )
    """
    Description: Identifies why a request to add (or activate) a record is being
    refused.  Examples include the receiving system not able to match the
    identifier and find that record in the receiving system, having no permission,
    or a detected issue exists which precludes the requested action.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    RefusalReasonCode = SubstanceAdminSubstitutionReason("_RefusalReasonCode")
    """
    Reasons for cancelling or rescheduling an Appointment
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    SchedulingActReason = SubstanceAdminSubstitutionReason("_SchedulingActReason")
    """
    Indicates why the act revision (status update) is being refused.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    StatusRevisionRefusalReasonCode = SubstanceAdminSubstitutionReason(
        "_StatusRevisionRefusalReasonCode"
    )
    """
    Definition:Indicates why the requested authorization to prescribe or dispense
    a medication has been refused.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    SubstanceAdministrationPermissionRefusalReasonCode = (
        SubstanceAdminSubstitutionReason(
            "_SubstanceAdministrationPermissionRefusalReasonCode"
        )
    )
    """
    Reasons why substitution of a substance administration request is not
    permitted.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    SubstanceAdminSubstitutionNotAllowedReason = SubstanceAdminSubstitutionReason(
        "_SubstanceAdminSubstitutionNotAllowedReason"
    )
    """
    SubstanceAdminSubstitutionReason
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    SubstanceAdminSubstitutionReason_ = SubstanceAdminSubstitutionReason(
        "_SubstanceAdminSubstitutionReason"
    )
    """
    The explanation for why a patient is moved from one location to another within
    the organization
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    TransferActReason = SubstanceAdminSubstitutionReason("_TransferActReason")
    """
    Definition: This domain is used to document reasons for providing a billable
    service; the billable services may include both clinical services and social
    services.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ActBillableServiceReason = SubstanceAdminSubstitutionReason(
        "_ActBillableServiceReason"
    )
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    BONUS = SubstanceAdminSubstitutionReason("BONUS")
    """
    Description:The level of coverage under the policy or program is available
    only to children
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    ChildrenOnly = SubstanceAdminSubstitutionReason("CHD")
    """
    Description:The level of coverage under the policy or program is available
    only to a subscriber's dependents.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    DependentsOnly = SubstanceAdminSubstitutionReason("DEP")
    """
    Description:The level of coverage under the policy or program is available to
    an employee and his or her children.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    EmployeeAndChildren = SubstanceAdminSubstitutionReason("ECH")
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    EDU = SubstanceAdminSubstitutionReason("EDU")
    """
    Description:The level of coverage under the policy or program is available
    only to an employee.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    EmployeeOnly = SubstanceAdminSubstitutionReason("EMP")
    """
    Description:The level of coverage under the policy or program is available to
    an employee and his or her spouse.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    EmployeeAndSpouse = SubstanceAdminSubstitutionReason("ESP")
    """
    Description:The level of coverage under the policy or program is available to
    a subscriber's family.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    Family = SubstanceAdminSubstitutionReason("FAM")
    """
    Description:The level of coverage under the policy or program is available to
    an individual.
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    Individual = SubstanceAdminSubstitutionReason("IND")
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    INVOICE = SubstanceAdminSubstitutionReason("INVOICE")
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    PROA = SubstanceAdminSubstitutionReason("PROA")
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    RECOV = SubstanceAdminSubstitutionReason("RECOV")
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    RETRO = SubstanceAdminSubstitutionReason("RETRO")
    """
    Description:The level of coverage under the policy or program is available to
    a subscriber's spouse and children
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    SpouseAndChildren = SubstanceAdminSubstitutionReason("SPC")
    """
    Description:The level of coverage under the policy or program is available
    only to a subscribers spouse
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    SpouseOnly = SubstanceAdminSubstitutionReason("SPO")
    """
    From: http://terminology.hl7.org/CodeSystem/v3-ActReason in v3-codesystems.xml
    """
    TRAN = SubstanceAdminSubstitutionReason("TRAN")
