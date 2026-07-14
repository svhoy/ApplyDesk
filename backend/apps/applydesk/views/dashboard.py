from django.db.models import Count
from django.shortcuts import render

from apps.applydesk.models import Application
from apps.applydesk.queries.applications import get_activity
from apps.applydesk.services.analytics import (
    get_bottleneck,
    get_stuck_applications,
    get_time_in_status,
    get_top_priorities,
)


def dashboard(request):

    stats = Application.objects.values("status").annotate(total=Count("id"))

    status_map = {item["status"]: item["total"] for item in stats}

    pipeline_statuses = [
        "saved",
        "pre_screen",
        "prepared",
        "applied",
        "waiting",
        "interview",
        "offer",
    ]

    pipeline = [
        {
            "status": status,
            "count": status_map.get(status, 0),
        }
        for status in pipeline_statuses
    ]

    total_active = sum(item["count"] for item in pipeline)
    saved = status_map.get("saved", 0)
    applied = status_map.get("applied", 0)
    interview = status_map.get("interview", 0)
    offer = status_map.get("offer", 0)

    conversion = {
        "saved_to_applied": round((applied / saved) * 100, 1) if saved else 0,
        "applied_to_interview": round((interview / applied) * 100, 1) if applied else 0,
        "interview_to_offer": round((offer / interview) * 100, 1) if interview else 0,
    }

    activity = get_activity()

    time_in_status = get_time_in_status()

    avg_time_in_status = {
        status: sum(times) / len(times)
        for status, times in time_in_status.items()
        if times
    }
    bottleneck = get_bottleneck(avg_time_in_status)

    stuck_applications = get_stuck_applications()

    top_priorities = get_top_priorities()
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "pipeline": pipeline,
            "status_map": status_map,
            "total_active": total_active,
            "conversion": conversion,
            "activity": activity,
            "avg_time_in_status": avg_time_in_status,
            "bottleneck": bottleneck,
            "stuck_applications": stuck_applications,
            "top_priorities": top_priorities,
        },
    )
