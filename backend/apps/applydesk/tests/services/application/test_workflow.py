import pytest

from apps.applydesk.services.applications.workflow import (
    get_available_actions,
)


@pytest.mark.django_db
def test_saved_actions(application):

    application.status = "saved"

    actions = get_available_actions(application)

    action_to_values = {a["to"] for a in actions}

    assert {"closed", "prepared"} == action_to_values


@pytest.mark.django_db
def test_saved_actions_with_contact(application):

    application.status = "saved"
    application.contact_email = "test@test.de"

    actions = get_available_actions(application)

    action_to_values = {a["to"] for a in actions}

    assert {"closed", "pre_screen", "prepared"} == action_to_values
