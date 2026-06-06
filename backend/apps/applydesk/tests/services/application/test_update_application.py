import pytest

from apps.applydesk.services.applications.transition import (
    transition_application,
)


@pytest.mark.django_db
def test_valid_transition(application):

    transition_application(application, "prepared")

    application.refresh_from_db()

    assert application.status == "prepared"


@pytest.mark.django_db
def test_invalid_transition(application):

    with pytest.raises(ValueError):
        transition_application(application, "offer")
