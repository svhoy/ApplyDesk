from django.db import transaction

from apps.applydesk.services.documents.schema_validation import (
    validate_schema,
)
from apps.applydesk.services.documents.schema_version import (
    create_schema_version,
)


@transaction.atomic
def publish_schema(*, schema):

    errors = validate_schema(schema)

    if errors:
        return {
            "success": False,
            "errors": errors,
        }

    draft = schema.draft_version()

    if not draft:
        return {
            "success": False,
            "errors": ["No draft version exists."],
        }

    # bisherigen Draft veröffentlichen

    draft.status = "published"
    draft.save(update_fields=["status"])

    # neue Draft Version erzeugen

    create_schema_version(
        schema=schema,
        status="draft",
        data={
            "fields": draft.data.get(
                "fields",
                [],
            )
        },
    )

    return {
        "success": True,
        "version": draft,
    }
