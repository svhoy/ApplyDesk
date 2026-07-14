from apps.applydesk.models import (
    Application,
    ApplicationRequiredDocument,
    ApplicationStatusHistory,
    Company,
)


def create_application(*, company_name: str, required_documents=None, **data):
    def normalize_company_name(name: str) -> str:
        return name.strip().title()

    normalized_company_name = normalize_company_name(company_name)
    company, created = Company.objects.get_or_create(
        name=normalized_company_name,
    )

    application = Application.objects.create(company=company, **data)
    ApplicationStatusHistory.objects.create(
        application=application,
        from_status=None,
        to_status=application.status,  # "saved"
    )
    if required_documents:
        ApplicationRequiredDocument.objects.bulk_create(
            [
                ApplicationRequiredDocument(
                    application=application,
                    document_type=doc,
                )
                for doc in required_documents
            ]
        )

    return application
