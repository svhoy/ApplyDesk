from django.db.models import Count

from apps.applydesk.models import Company


def list_companies():
    return Company.objects.annotate(
        application_count=Count(
            "application",
        )
    ).order_by("name")


def get_company(company_id):
    return (
        Company.objects.annotate(
            application_count=Count(
                "application",
            )
        )
        .prefetch_related(
            "application_set",
        )
        .get(pk=company_id)
    )
