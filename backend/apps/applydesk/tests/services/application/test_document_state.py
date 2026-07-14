import pytest

from apps.applydesk.models import ApplicationDocument
from apps.applydesk.services.applications.document_state import (
    get_application_document_state,
)


@pytest.mark.django_db
def test_document_state_returns_missing_documents(
    application_with_requirements,
):

    state = get_application_document_state(
        application_with_requirements,
    )

    assert state["missing"] == {
        "cv",
        "cover_letter",
    }


@pytest.mark.django_db
def test_document_state_with_uploaded_cv(
    application_with_requirements,
    document_factory,
):

    cv = document_factory(
        document_type="cv",
    )

    ApplicationDocument.objects.create(
        application=application_with_requirements,
        document=cv,
    )

    state = get_application_document_state(
        application_with_requirements,
    )

    assert state["missing"] == {
        "cover_letter",
    }


def test_document_state_contains_labels(
    application_with_requirements,
):

    state = get_application_document_state(
        application_with_requirements,
    )

    assert state["documents"] == [
        {
            "type": "cover_letter",
            "label": "Cover Letter",
            "attached": False,
        },
        {
            "type": "cv",
            "label": "CV",
            "attached": False,
        },
    ]
