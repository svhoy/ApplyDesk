from apps.applydesk.models import (
    DocumentSchema,
)


def get_document_schema(
    schema_id,
):

    return DocumentSchema.objects.get(
        pk=schema_id,
    )


def list_document_schemas():

    return DocumentSchema.objects.order_by(
        "document_type",
        "name",
    )


def get_active_template(document_type):

    return DocumentSchema.objects.filter(
        document_type=document_type, is_default=True
    ).first()
