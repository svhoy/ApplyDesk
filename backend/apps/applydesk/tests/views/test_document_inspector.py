import pytest
from django.urls import reverse

from apps.applydesk.models import Document


@pytest.mark.django_db
def test_document_inspector_view(client):

    doc = Document.objects.create(
        title="CV",
        document_type="cv",
        file="dummy.pdf",
    )

    response = client.get(
        reverse(
            "document_inspector",
            args=[doc.id],  # ty:ignore[unresolved-attribute]
        ),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert "CV" in response.content.decode()
