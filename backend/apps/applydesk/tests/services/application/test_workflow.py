import pytest

from apps.applydesk.services.applications.workflow import (
    get_available_actions,
)


@pytest.mark.django_db
def test_saved_actions(application):

    application.status = "saved"

    actions = get_available_actions(application)

    assert len(actions) == 1
    assert actions[0]["to"] == "prepared"
