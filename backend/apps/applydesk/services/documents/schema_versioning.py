from copy import deepcopy

from apps.applydesk.models import (
    DocumentSchemaVersion,
)
from apps.applydesk.models.document import DocumentSchemaVersionStatus
from apps.applydesk.services.documents.schema_version import (
    create_schema_version,
)


def get_or_create_draft(schema):
    draft = schema.draft_version()

    if draft:
        return draft

    return create_schema_version(
        schema=schema,
        status=DocumentSchemaVersionStatus.DRAFT,
    )


def publish_schema(schema):
    draft = schema.draft_version()

    if not draft:
        raise ValueError("No draft")

    latest = schema.latest_published_version()

    next_version = (latest.version + 1) if latest else 1

    create_schema_version(
        schema=schema,
        status="published",
        version=next_version,
        data=draft.data,
    )

    return schema


def restore_version(
    *,
    schema,
    version,
):
    draft = schema.draft_version()

    if draft:
        draft.delete()

    create_schema_version(
        schema=schema,
        status=DocumentSchemaVersionStatus.DRAFT,
        data=version.data,
    )
