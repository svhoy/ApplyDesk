import pytest
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)

from apps.applydesk.models import Document


@pytest.mark.django_db
def test_document_creation():

    document = Document.objects.create(
        title="CV",
        document_type="cv",
        file=SimpleUploadedFile(
            "cv.pdf",
            b"dummy pdf",
        ),
    )

    assert document.pk is not None