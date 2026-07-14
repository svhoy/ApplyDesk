from copy import deepcopy

from apps.applydesk.models import (
    DocumentSchemaVersion,
)


def create_schema_version(
    *,
    schema,
    status,
    data=None,
    version=None,
):
    if version is None:
        latest = schema.latest_version()

        version = 1 if latest is None else latest.version + 1

    return DocumentSchemaVersion.objects.create(
        schema=schema,
        status=status,
        version=version,
        data=deepcopy(data or {"fields": []}),
    )