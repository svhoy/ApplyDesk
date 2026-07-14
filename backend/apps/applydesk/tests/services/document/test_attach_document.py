import pytest

from apps.applydesk.models import ApplicationDocument
from apps.applydesk.services.documents.attach_document import (
    attach_document_to_application,
    detach_document_from_application,
)


@pytest.mark.django_db
def test_attach_document_service(
    application,
    document_factory,
):

    document = document_factory()

    link = attach_document_to_application(
        application=application,
        document=document,
    )

    assert link.application == application
    assert link.document == document


@pytest.mark.django_db
def test_detach_document_service(
    application,
    document_factory,
):

    document = document_factory()

    link = ApplicationDocument.objects.create(
        application=application,
        document=document,
    )

    detach_document_from_application(
        link=link,
    )

    assert ApplicationDocument.objects.count() == 0
