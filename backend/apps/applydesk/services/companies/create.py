from apps.applydesk.models import Company


def create_company(
    **data,
):
    company, _ = Company.objects.get_or_create(
        name=data["name"],
        defaults=data,
    )

    return company
