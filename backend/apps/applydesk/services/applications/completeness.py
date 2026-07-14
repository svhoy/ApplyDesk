from apps.applydesk.services.applications.document_state import (
    get_application_document_state,
)


def calculate_application_completeness_from_state(
    state,
):

    required = state["required"]

    if not required:
        return 0

    completed = len(
        state["attached"] & required,
    )

    return int(
        completed / len(required) * 100,
    )


def calculate_application_completeness(
    application,
):

    state = get_application_document_state(
        application,
    )

    return calculate_application_completeness_from_state(
        state,
    )
