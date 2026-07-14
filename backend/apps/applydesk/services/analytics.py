from collections import defaultdict
from datetime import timedelta

from django.utils import timezone

from apps.applydesk.models import Application
from apps.applydesk.services.attention_score import (
    explain_attention_score,
)


def get_time_in_status():

    time_map = defaultdict(list)
    now = timezone.now()

    applications = Application.objects.prefetch_related("history")

    for app in applications:
        history = list(app.history.all().order_by("created_at"))  # ty:ignore[unresolved-attribute]

        if not history:
            continue

        if (
            len(history) > 1
        ):  # checke die länge, wenn ausschließlich saved vorhanden ist, wird es im letzten Schritt bestimmt
            time_map["saved"].append((now - app.created_at).total_seconds())

        for i in range(len(history) - 1):
            curr = history[i]
            next_h = history[i + 1]

            duration = next_h.created_at - curr.created_at

            time_map[curr.to_status].append(duration.total_seconds())

        last = history[-1]

        time_map[last.to_status].append((now - last.created_at).total_seconds())

    return time_map


def get_bottleneck(avg_time_in_status):

    if not avg_time_in_status:
        return None

    status = max(
        avg_time_in_status,
        key=avg_time_in_status.get,
    )

    return {
        "status": status,
        "duration": avg_time_in_status[status],
    }


ATTENTION_THRESHOLD_DAYS = 7


def get_stuck_applications():

    threshold = timezone.now() - timedelta(days=ATTENTION_THRESHOLD_DAYS)

    return (
        Application.objects.exclude(
            status__in=["offer", "rejected", "archived", "closed"]
        )
        .filter(status_changed_at__lt=threshold)
        .select_related("company")
    )


def get_top_priorities(limit=5):

    applications = Application.objects.select_related("company").exclude(
        status__in=["rejected", "archived", "closed"]
    )

    scored = []

    for app in applications:
        explanation = explain_attention_score(app)

        scored.append(
            {
                "application": app,
                "score": explanation["score"],
                "breakdown": explanation["breakdown"],
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:limit]
