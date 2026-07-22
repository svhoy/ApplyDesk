from copy import deepcopy

from apps.applydesk.models import DocumentSchema
from apps.applydesk.models.versioned import VersionStatus
from apps.applydesk.services.documents.schema_versioning import get_or_create_draft


def create_schema(
    *,
    name: str,
    document_type: str,
) -> DocumentSchema:

    schema = DocumentSchema.objects.create(
        name=name,
        document_type=document_type,
        schema={"fields": []},
    )

    get_or_create_draft(schema)

    return schema


def update_schema(
    *,
    schema: DocumentSchema,
    name: str,
    document_type: str,
) -> DocumentSchema:
    schema.name = name
    schema.document_type = document_type

    schema.save(
        update_fields=[
            "name",
            "document_type",
        ],
    )

    return schema


def duplicate_schema(*, schema):
    new_schema = create_schema(
        name=f"{schema.name} (Copy)",
        document_type=schema.document_type,
    )

    old_version = schema.draft_version or schema.latest_version

    new_draft = new_schema.draft_version

    # NUR UPDATE, NICHT NEU ERZEUGEN
    new_draft.data = deepcopy(old_version.data if old_version else {"fields": []})
    new_draft.save()

    return new_schema


def publish_version(schema):
    draft = schema.draft_version

    if not draft:
        return None

    draft.status = VersionStatus.PUBLISHED
    draft.save(update_fields=["status"])

    # neue Draft erzeugen
    return get_or_create_draft(schema)
