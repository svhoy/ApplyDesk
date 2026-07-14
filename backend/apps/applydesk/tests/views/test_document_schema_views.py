import pytest
from django.urls import reverse

from apps.applydesk.models import DocumentSchema
from apps.applydesk.services.documents.schema import create_schema


@pytest.mark.django_db
def test_schema_editor_view(client):

    schema = create_schema(
        name="Cover Letter",
        document_type="cover_letter",
    )

    response = client.get(
        reverse(
            "schema_editor",
            args=[schema.pk],
        )
    )

    assert response.status_code == 200
    assert "Cover Letter" in response.content.decode()


@pytest.mark.django_db
def test_document_page_shows_schemas(
    client,
):

    DocumentSchema.objects.create(
        name="Modern CV",
        document_type="cv",
        schema={
            "fields": [],
        },
    )

    response = client.get(
        reverse("document_list"),
    )

    assert "Modern CV" in response.content.decode()
