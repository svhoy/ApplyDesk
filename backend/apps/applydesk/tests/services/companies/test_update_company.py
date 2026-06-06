import pytest

from apps.applydesk.services.companies.update import (
    update_company,
)


@pytest.mark.django_db
def test_update_company(company):

    update_company(
        company,
        url="https://google.com",
    )

    company.refresh_from_db()

    assert company.url == "https://google.com"
