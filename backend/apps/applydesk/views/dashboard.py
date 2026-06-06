from django.db.models import Count
from django.shortcuts import render

from apps.applydesk.models import Application


def dashboard(request):
    stats = Application.objects.values("status").annotate(total=Count("id"))

    status_map = {item["status"]: item["total"] for item in stats}

    total_applications = Application.objects.count()

    active = Application.objects.exclude(status="archived").count()

    interviews = status_map.get("interview", 0)
    offers = status_map.get("offer", 0)
    rejected = status_map.get("rejected", 0)

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total_applications": total_applications,
            "active": active,
            "interviews": interviews,
            "offers": offers,
            "rejected": rejected,
            "status_map": status_map,
        },
    )
