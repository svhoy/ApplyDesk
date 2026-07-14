from django.utils import timezone

from apps.applydesk.models import ApplicationStatusHistory
from apps.applydesk.services.applications.workflow import WORKFLOW_ACTIONS


def transition_application(application, new_status: str):

    allowed_actions = WORKFLOW_ACTIONS.get(application.status, [])

    allowed_targets = [action["to"] for action in allowed_actions]

    if new_status not in allowed_targets:
        raise ValueError(f"Invalid transition: {application.status} → {new_status}")

    old_status = application.status

    application.status = new_status
    application.status_changed_at = timezone.now()
    application.save()

    ApplicationStatusHistory.objects.create(
        application=application,
        from_status=old_status,
        to_status=new_status,
    )

    return application
