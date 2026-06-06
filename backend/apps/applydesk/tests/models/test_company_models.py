import pytest


@pytest.mark.django_db
def test_company_created(company):

    assert company.name == "Google"
