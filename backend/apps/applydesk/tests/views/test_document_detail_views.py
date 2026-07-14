import pytest
from django.urls import reverse

from apps.applydesk.models import Document


@pytest.mark.django_db
def test_document_detail_view(client):

    doc = Document.objects.create(
        title="CV",
        document_type="cv",
        file="dummy.pdf",
    )

    response = client.get(
        reverse(
            "document_detail",
            args=[doc.id],
        )
    )

    assert response.status_code == 200
    assert "CV" in response.content.decode()


@pytest.mark.django_db
def test_document_detail_shows_applications(
    client,
    application,
):

    doc = Document.objects.create(
        title="CV",
        document_type="cv",
        file="dummy.pdf",
    )

    from apps.applydesk.models import ApplicationDocument

    ApplicationDocument.objects.create(
        application=application,
        document=doc,
    )

    response = client.get(
        reverse(
            "document_detail",
            args=[doc.id],
        )
    )

    assert application.company.name in response.content.decode()
