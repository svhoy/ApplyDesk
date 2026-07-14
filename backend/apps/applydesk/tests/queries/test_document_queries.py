import pytest

from apps.applydesk.models import ApplicationDocument
from apps.applydesk.queries.document import (
    get_attached_document_types,
    get_required_document_types,
)


@pytest.mark.django_db
def test_get_required_document_types(application_with_requirements):

    result = get_required_document_types(
        application_with_requirements,
    )

    assert set(result) == {
        "cv",
        "cover_letter",
    }


@pytest.mark.django_db
def test_get_attached_document_types(
    application,
    document_factory,
):

    cv = document_factory(
        document_type="cv",
    )

    ApplicationDocument.objects.create(
        application=application,
        document=cv,
    )

    result = get_attached_document_types(
        application,
    )

    assert result == {"cv"}
