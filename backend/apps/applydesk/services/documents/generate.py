from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from weasyprint import HTML

from apps.applydesk.models import ApplicationDocument, Document
from apps.applydesk.queries.document_schema import get_active_template


def generate_document(
    *,
    application,
    document_type: str,
    field_values: dict,
) -> Document:

    template = get_active_template(document_type)

    if not template:
        raise ValueError(f"No template found for {document_type}")

    context = {
        "application": application,
        "company": application.company,
        "position_title": application.position_title,
        "fields": field_values,
    }

    html_string = render_to_string(
        template.template_html,
        context,
    )

    pdf_file = HTML(string=html_string).write_pdf()

    document = Document.objects.create(
        title=f"{template.name} - {application.company.name}",
        document_type=document_type,
    )

    filename = f"{document_type}_{application.id}.pdf"

    document.file.save(
        filename,
        ContentFile(pdf_file),
        save=True,
    )

    ApplicationDocument.objects.create(
        application=application,
        document=document,
    )

    return document
