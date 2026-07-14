import pytest

from apps.applydesk.services.applications.create import (
    create_application,
)


@pytest.mark.django_db
def test_create_application_reuses_company():

    create_application(
        company_name="Google",
        position_title="Backend Engineer",
    )

    from apps.applydesk.models import Company

    assert Company.objects.count() == 1


def test_application_creates_initial_history(db):

    app = create_application(
        company_name="Google",
        position_title="Engineer",
    )

    assert app.history.count() == 1

    entry = app.history.first()

    assert entry.from_status is None
    assert entry.to_status == "saved"
