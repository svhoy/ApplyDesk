from apps.applydesk.models import Company


def delete_company(company):
    if company.application_set.exists():
        raise ValueError("Company has applications")

    company.delete()
