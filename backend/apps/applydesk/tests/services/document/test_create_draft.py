import pytest

from apps.applydesk.services.documents.draft import create_draft, update_draft


@pytest.mark.django_db
def test_create_draft(application):
    draft = create_draft(
        application=application,
        document_type="cover_letter",
        field_values={"main_text": "Hello"},
    )

    assert draft.field_values["main_text"] == "Hello"


@pytest.mark.django_db
def test_update_draft(application):

    draft = create_draft(
        application=application,
        document_type="cover_letter",
        field_values={
            "main_text": "Hello",
        },
    )

    updated = update_draft(
        draft,
        {
            "main_text": "Updated",
        },
    )

    assert updated.field_values["main_text"] == "Updated"
