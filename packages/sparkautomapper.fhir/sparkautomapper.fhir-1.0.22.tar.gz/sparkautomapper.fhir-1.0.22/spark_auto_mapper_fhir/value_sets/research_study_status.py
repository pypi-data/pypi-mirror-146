from __future__ import annotations

from spark_auto_mapper_fhir.fhir_types.uri import FhirUri

from spark_auto_mapper_fhir.value_sets.generic_type import GenericTypeCode
from spark_auto_mapper.type_definitions.defined_types import AutoMapperTextInputType


# This file is auto-generated by generate_classes so do not edit manually
# noinspection PyPep8Naming
class ResearchStudyStatusCode(GenericTypeCode):
    """
    ResearchStudyStatus
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
        Codes that convey the current status of the research study.
    """

    def __init__(self, value: AutoMapperTextInputType):
        super().__init__(value=value)

    """
    http://hl7.org/fhir/research-study-status
    """
    codeset: FhirUri = "http://hl7.org/fhir/research-study-status"


class ResearchStudyStatusCodeValues:
    """
    Study is opened for accrual.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """

    Active = ResearchStudyStatusCode("active")
    """
    Study is completed prematurely and will not resume; patients are no longer
    examined nor treated.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    AdministrativelyCompleted = ResearchStudyStatusCode("administratively-completed")
    """
    Protocol is approved by the review board.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    Approved = ResearchStudyStatusCode("approved")
    """
    Study is closed for accrual; patients can be examined and treated.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    ClosedToAccrual = ResearchStudyStatusCode("closed-to-accrual")
    """
    Study is closed to accrual and intervention, i.e. the study is closed to
    enrollment, all study subjects have completed treatment or intervention but
    are still being followed according to the primary objective of the study.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    ClosedToAccrualAndIntervention = ResearchStudyStatusCode(
        "closed-to-accrual-and-intervention"
    )
    """
    Study is closed to accrual and intervention, i.e. the study is closed to
    enrollment, all study subjects have completed treatment
    or intervention but are still being followed according to the primary
    objective of the study.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    Completed = ResearchStudyStatusCode("completed")
    """
    Protocol was disapproved by the review board.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    Disapproved = ResearchStudyStatusCode("disapproved")
    """
    Protocol is submitted to the review board for approval.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    InReview = ResearchStudyStatusCode("in-review")
    """
    Study is temporarily closed for accrual; can be potentially resumed in the
    future; patients can be examined and treated.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    TemporarilyClosedToAccrual = ResearchStudyStatusCode(
        "temporarily-closed-to-accrual"
    )
    """
    Study is temporarily closed for accrual and intervention and potentially can
    be resumed in the future.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    TemporarilyClosedToAccrualAndIntervention = ResearchStudyStatusCode(
        "temporarily-closed-to-accrual-and-intervention"
    )
    """
    Protocol was withdrawn by the lead organization.
    From: http://hl7.org/fhir/research-study-status in valuesets.xml
    """
    Withdrawn = ResearchStudyStatusCode("withdrawn")
