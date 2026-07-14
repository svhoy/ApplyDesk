import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.applydesk.models import ApplicationDocument


@pytest.mark.django_db
def test_attach_modal_opens(
    client,
    application,
):

    response = client.get(
        reverse(
            "attach_document_modal",
            args=[application.id],
        ),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert "Attach Document" in response.content.decode()


@pytest.mark.django_db
def test_attach_document(
    client,
    application,
    document_factory,
):

    doc = document_factory()

    response = client.post(
        reverse(
            "attach_document",
            args=[application.id, doc.id],
        ),
        HTTP_HX_REQUEST="true",
    )

    assert ApplicationDocument.objects.count() == 1


@pytest.mark.django_db
def test_detach_document(
    client,
    application,
    document_factory,
):

    doc = document_factory()

    link = ApplicationDocument.objects.create(
        application=application,
        document=doc,
    )

    response = client.post(
        reverse(
            "detach_document",
            args=[link.id],  # ty:ignore[unresolved-attribute]
        ),
        HTTP_HX_REQUEST="true",
    )

    assert ApplicationDocument.objects.count() == 0


@pytest.mark.django_db
def test_upload_document_for_application(
    client,
    application,
):

    response = client.post(
        reverse(
            "upload_document_for_application",
            args=[application.id],
        ),
        {
            "document_type": "cv",
            "file": SimpleUploadedFile(
                "cv.pdf",
                b"pdf content",
            ),
        },
    )

    assert response.status_code == 200

    assert application.application_documents.count() == 1
