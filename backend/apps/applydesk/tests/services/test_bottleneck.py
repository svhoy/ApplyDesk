from datetime import timedelta

import pytest
from django.utils import timezone

from apps.applydesk.services.analytics import get_bottleneck, get_stuck_applications


def test_returns_longest_status():

    avg_time = {
        "saved": 100,
        "prepared": 300,
        "applied": 900,
        "interview": 200,
    }

    result = get_bottleneck(avg_time)

    assert result["status"] == "applied"
    assert result["duration"] == 900


@pytest.mark.django_db
def test_detects_stuck_application(application_factory):

    app = application_factory(
        status="applied",
    )

    app.status_changed_at = timezone.now() - timedelta(days=10)
    app.save()

    result = get_stuck_applications()

    assert len(result) == 1
    assert result[0].id == app.id
