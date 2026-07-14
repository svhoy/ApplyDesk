import pytest

from apps.applydesk.models import (
    Application,
    ApplicationDocument,
    Document,
)


@pytest.mark.django_db
def test_application_fixture(application):

    assert application.company.name == "Google"
    assert application.position_title == "Engineer"


@pytest.mark.django_db
def test_application_document_creation(
    application,
):

    doc = Document.objects.create(
        title="CV",
        document_type="cv",
        file="dummy.pdf",
    )

    link = ApplicationDocument.objects.create(
        application=application,
        document=doc,
    )

    assert link.pk is not None


@pytest.mark.django_db
def test_unique_constraint(
    application,
):

    doc = Document.objects.create(
        title="CV",
        document_type="cv",
        file="dummy.pdf",
    )

    ApplicationDocument.objects.create(
        application=application,
        document=doc,
    )

    with pytest.raises(Exception):
        ApplicationDocument.objects.create(
            application=application,
            document=doc,
        )
