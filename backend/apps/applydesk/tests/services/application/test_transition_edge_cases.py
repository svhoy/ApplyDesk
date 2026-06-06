import pytest

from apps.applydesk.services.applications.transition import (
    transition_application,
)


@pytest.mark.django_db
def test_invalid_transition(application):

    with pytest.raises(ValueError):
        transition_application(application, "offer")
