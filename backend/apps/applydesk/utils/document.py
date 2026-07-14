from apps.applydesk.models.document import DocumentType


def get_document_label(document_type: str) -> str:
    return DocumentType(document_type).label
