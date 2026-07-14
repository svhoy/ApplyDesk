import pytest

from apps.applydesk.models import (
    ApplicationDocument,
)
from apps.applydesk.services.applications.completeness import (
    calculate_application_completeness,
)


@pytest.mark.django_db
def test_empty_application_is_zero_percent(
    application,
):

    result = calculate_application_completeness(
        application,
    )

    assert result == 0


@pytest.mark.django_db
def test_cv_is_fifty_percent(
    application_with_requirements,
    document_factory,
):

    cv = document_factory(
        document_type="cv",
    )

    ApplicationDocument.objects.create(
        application=application_with_requirements,
        document=cv,
    )

    result = calculate_application_completeness(
        application_with_requirements,
    )

    assert result == 50
