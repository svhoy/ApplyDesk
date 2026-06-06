from apps.applydesk.models import Application, Company


def create_application(*, company_name: str, **data):
    def normalize_company_name(name: str) -> str:
        return name.strip().title()

    normalized_company_name = normalize_company_name(company_name)
    company, created = Company.objects.get_or_create(
        name=normalized_company_name,
    )

    application = Application.objects.create(company=company, **data)

    return application
