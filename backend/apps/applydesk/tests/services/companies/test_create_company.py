import pytest

from apps.applydesk.models import Company
from apps.applydesk.services.companies.create import (
    create_company,
)


@pytest.mark.django_db
def test_create_company():

    company = create_company(
        name="Google",
    )

    assert company.name == "Google"


@pytest.mark.django_db
def test_create_company_reuses_existing():

    Company.objects.create(
        name="Google",
    )

    create_company(
        name="Google",
    )

    assert Company.objects.count() == 1
