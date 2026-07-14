import pytest

from apps.applydesk.services.analytics import get_time_in_status


@pytest.mark.django_db
def test_time_in_status_basic_flow(
    application_factory,
    history_factory,
):

    app = application_factory(
        status="saved",
    )

    history_factory(
        application=app,
        from_status="saved",
        to_status="prepared",
    )

    history_factory(
        application=app,
        from_status="prepared",
        to_status="applied",
    )

    result = get_time_in_status()

    assert "saved" in result
    assert len(result["saved"]) == 1
