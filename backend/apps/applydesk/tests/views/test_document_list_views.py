import pytest
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
from django.urls import reverse

from apps.applydesk.models import Document


@pytest.mark.django_db
def test_document_list_view(client):

    response = client.get(reverse("document_list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_document_upload(client):

    file = SimpleUploadedFile(
        "cv.pdf",
        b"test",
    )

    response = client.post(
        reverse("upload_document"),
        {
            "title": "CV",
            "document_type": "cv",
            "file": file,
            "action": "upload",
        },
    )

    assert response.status_code == 200

    assert Document.objects.count() == 1
