import pytest

from apps.applydesk.services.applications.transition import transition_application


@pytest.mark.django_db
def test_history_is_written_on_transition(application_factory):

    app = application_factory(status="saved")

    transition_application(app, "prepared")

    assert app.history.count() == 1

    entry = app.history.first()

    assert entry.from_status == "saved"
    assert entry.to_status == "prepared"
