from datetime import timedelta

from django.utils import timezone

from apps.applydesk.services.time_format import format_duration

APPLICATION_PRIORITY_WEIGHT = {
    "A": 100,
    "B": 50,
    "C": 20,
    "I": 70,
}

COMPANY_PRIORITY_WEIGHT = {
    "A": 100,
    "B": 50,
    "C": 20,
}

STATUS_WEIGHT = {
    "saved": 10,
    "pre_screen": 30,
    "prepared": 20,
    "applied": 50,
    "waiting": 60,
    "interview": 90,
    "offer": 100,
}


def calculate_attention_score(application):

    score = 0

    score += APPLICATION_PRIORITY_WEIGHT.get(
        application.priority,
        0,
    )

    score += COMPANY_PRIORITY_WEIGHT.get(
        application.company.priority,
        0,
    )

    score += STATUS_WEIGHT.get(
        application.status,
        0,
    )

    if hasattr(application, "status_changed_at"):
        days = (timezone.now() - application.status_changed_at).days

        score += min(days * 5, 50)

    return score




def explain_attention_score(application):

    breakdown = []

    score = 0

    # ─────────────────────────────
    # Company priority
    # ─────────────────────────────
    company_score = COMPANY_PRIORITY_WEIGHT.get(
        application.company.priority,
        0,
    )

    score += company_score

    breakdown.append({
        "label": f"Company priority ({application.company.priority})",
        "value": company_score,
    })

    # ─────────────────────────────
    # Application priority
    # ─────────────────────────────
    app_score = APPLICATION_PRIORITY_WEIGHT.get(
        application.priority,
        0,
    )

    score += app_score

    breakdown.append({
        "label": f"Application priority ({application.priority})",
        "value": app_score,
    })

    # ─────────────────────────────
    # Status score
    # ─────────────────────────────
    status_score = STATUS_WEIGHT.get(
        application.status,
        0,
    )

    score += status_score

    breakdown.append({
        "label": f"Status ({application.status})",
        "value": status_score,
    })

    # ─────────────────────────────
    # Age factor
    # ─────────────────────────────
    if hasattr(application, "status_changed_at"):

        days = (
            timezone.now()
            - application.status_changed_at
        ).days

        age_score = min(days * 5, 50)

        score += age_score

        breakdown.append({
            "label": f"Time in status ({days} days)",
            "value": age_score,
        })

    return {
        "score": score,
        "breakdown": breakdown,
    }