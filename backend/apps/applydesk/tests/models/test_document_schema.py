import pytest

from apps.applydesk.models import DocumentSchema


@pytest.mark.django_db
def test_document_schema_can_be_created():

    schema = DocumentSchema.objects.create(
        name="Cover Letter",
        document_type="cover_letter",
        schema={
            "fields": [],
        },
    )

    assert schema.pk is not None


@pytest.mark.django_db
def test_schema_stores_fields():

    schema = DocumentSchema.objects.create(
        name="Cover Letter",
        document_type="cover_letter",
        schema={
            "fields": [
                {
                    "name": "main_text",
                    "type": "textarea",
                }
            ]
        },
    )

    assert schema.schema["fields"][0]["name"] == "main_text"
