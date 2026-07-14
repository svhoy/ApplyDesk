import uuid
from pathlib import Path

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.applydesk.models import (
    Application,
    ApplicationStatusHistory,
    Company,
    Document,
    DocumentSchema,
)
from apps.applydesk.models.application import ApplicationRequiredDocument
from apps.applydesk.services.applications.create import create_application


@pytest.fixture(autouse=True)
def isolate_media_root(settings, tmp_path):
    """
    Override MEDIA_ROOT for all tests
    """

    settings.MEDIA_ROOT = tmp_path / "test_storage"

    Path(settings.MEDIA_ROOT).mkdir(
        parents=True,
        exist_ok=True,
    )


@pytest.fixture
def company(db):
    return Company.objects.create(name="Google")


@pytest.fixture
def application(company):
    return Application.objects.create(
        company=company,
        position_title="Engineer",
    )


@pytest.fixture
def created_application(db, company):
    return create_application(
        company_name="Google",
        position_title="Backend Engineer",
    )


@pytest.fixture
def application_with_requirements(application):

    ApplicationRequiredDocument.objects.create(
        application=application,
        document_type="cv",
    )

    ApplicationRequiredDocument.objects.create(
        application=application,
        document_type="cover_letter",
    )

    return application


@pytest.fixture
def application_factory(db):

    def create_app(**kwargs):

        company = Company.objects.create(
            name=f"Company-{uuid.uuid4()}",
            priority="B",
        )

        defaults = {
            "company": company,
            "position_title": "Engineer",
            "status": "saved",
            "priority": "B",
        }

        defaults.update(kwargs)

        return Application.objects.create(**defaults)

    return create_app


@pytest.fixture
def history_factory(db):

    def create_history(**kwargs):
        return ApplicationStatusHistory.objects.create(**kwargs)

    return create_history


@pytest.fixture
def document_factory(db):

    def create_document(**kwargs):

        defaults = {
            "title": "CV",
            "document_type": "cv",
            "file": SimpleUploadedFile(
                "cv.pdf",
                b"dummy content",
            ),
        }

        defaults.update(kwargs)

        return Document.objects.create(
            **defaults,
        )

    return create_document



@pytest.fixture
def schema(db):
    return DocumentSchema.objects.create(
        name="Test Schema",
        document_type="cv",
        schema={"fields": []},
    )
