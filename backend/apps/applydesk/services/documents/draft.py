from apps.applydesk.models import DocumentDraft


def create_draft(
    *,
    application,
    document_type,
    field_values=None,
):

    if field_values is None:
        field_values = {}

    return DocumentDraft.objects.create(
        application=application,
        document_type=document_type,
        field_values=field_values,
    )


def update_draft(
    draft,
    data: dict,
):

    draft.field_values.update(data)
    draft.save()

    return draft
