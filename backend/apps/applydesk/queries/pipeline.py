from collections import defaultdict

from apps.applydesk.models import Application
from apps.applydesk.services.applications.workflow import (
    get_available_actions,
)

PIPELINE_STATUSES = [
    "saved",
    "prepared",
    "applied",
    "waiting",
    "interview",
    "offer",
    "rejected",
]


def get_pipeline():

    columns = defaultdict(list)

    applications = (
        Application.objects.select_related("company").all().order_by("-created_at")
    )

    for app in applications:
        columns[app.status].append(
            {
                "object": app,
                "actions": get_available_actions(app),
            }
        )

    return columns
