import pytest


@pytest.mark.django_db
def test_application_fixture(application):

    assert application.company.name == "Google"
    assert application.position_title == "Engineer"
