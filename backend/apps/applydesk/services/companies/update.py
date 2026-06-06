from apps.applydesk.models import Company


def update_company(
    company: Company,
    **data,
):

    for field, value in data.items():
        setattr(
            company,
            field,
            value,
        )

    company.save()

    return company
