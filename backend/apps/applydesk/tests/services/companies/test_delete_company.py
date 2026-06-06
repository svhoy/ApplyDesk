import pytest

from apps.applydesk.services.companies.delete import delete_company


@pytest.mark.django_db
def test_delete_company(company):

    delete_company(company)

    assert company.pk is None or not company.__class__.objects.filter(pk=company.pk).exists()

@pytest.mark.django_db
def test_company_delete_blocked(company, application):

    with pytest.raises(ValueError):
        delete_company(company)


