import pytest
from django.urls import reverse

from apps.applydesk.models import Application, Company
from apps.applydesk.queries.companies import get_company, list_companies


@pytest.mark.django_db
def test_list_companies():

    Company.objects.create(
        name="Google",
    )

    Company.objects.create(
        name="Amazon",
    )

    result = list_companies()

    assert result.count() == 2


@pytest.mark.django_db
def test_company_application_count(
    company,
):
    Application.objects.create(
        company=company,
        position_title="Engineer",
    )

    result = list_companies()

    assert result.first().application_count == 1


@pytest.mark.django_db
def test_get_company(company):

    result = get_company(company.pk)

    assert result.pk == company.pk
