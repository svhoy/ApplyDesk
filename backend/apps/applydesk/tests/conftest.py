import pytest

from apps.applydesk.models import Application, Company
from apps.applydesk.services.applications.create import create_application


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
def created_application(db):
    return create_application(
        company_name="Google",
        position_title="Backend Engineer",
    )
