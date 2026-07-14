from apps.applydesk.models.document import DocumentType
from apps.applydesk.queries.document import (
    get_attached_document_types,
    get_required_document_types,
)


def get_application_document_state(application):

    required = get_required_document_types(
        application,
    )

    attached = get_attached_document_types(
        application,
    )

    documents = []

    for doc_type in sorted(required):
        documents.append(
            {
                "type": doc_type,
                "label": DocumentType(doc_type).label,
                "attached": doc_type in attached,
            }
        )

    return {
        "documents": documents,
        "required": required,
        "attached": attached,
        "missing": required - attached,
        "complete": required.issubset(attached),
    }
