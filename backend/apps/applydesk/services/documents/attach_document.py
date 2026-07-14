from apps.applydesk.models import (
    Application,
    ApplicationDocument,
    Document,
)
from apps.applydesk.services.documents.file_naming import (
    build_document_base_name,
    get_next_versioned_name,
)


def attach_document_to_application(
    *,
    application: Application,
    document: Document,
):

    link, _ = ApplicationDocument.objects.get_or_create(
        application=application,
        document=document,
    )

    return link


def detach_document_from_application(
    *,
    link: ApplicationDocument,
):

    link.delete()


def upload_document_to_application(
    *,
    application,
    document_type,
    file,
):

    base_name = build_document_base_name(
        document_type=document_type,
        company_name=application.company.name,
    )

    versioned_name = get_next_versioned_name(
        base_name=base_name,
    )

    document = Document.objects.create(
        title=versioned_name,
        document_type=document_type,
        file=file,
    )

    attach_document_to_application(
        application=application,
        document=document,
    )

    return document
