from apps.applydesk.queries.applications import (
    list_applications,
)
from apps.applydesk.services.applications.completeness import (
    calculate_application_completeness_from_state,
)
from apps.applydesk.services.applications.document_state import (
    get_application_document_state,
)


def list_applications_with_metrics():

    applications = list_applications()

    for application in applications:
        state = get_application_document_state(
            application,
        )

        application.document_state = state

        application.completeness = calculate_application_completeness_from_state(
            state,
        )

        application.required_document_count = len(
            state["required"],
        )

        application.attached_document_count = len(state["attached"] & state["required"])

        application.missing_document_count = len(
            state["missing"],
        )

    return applications
