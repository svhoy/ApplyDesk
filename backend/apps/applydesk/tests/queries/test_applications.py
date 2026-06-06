import pytest

from apps.applydesk.queries.applications import get_application, list_applications


@pytest.mark.django_db
def test_list_applications(application):

    result = list_applications()

    assert result.count() == 1





@pytest.mark.django_db
def test_get_application(
    application,
):
    result = get_application(
        application.pk,
    )

    assert result.pk == application.pk
