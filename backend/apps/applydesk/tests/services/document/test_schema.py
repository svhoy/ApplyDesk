from copy import deepcopy

import pytest

from apps.applydesk.services.documents.schema import (
    create_schema,
    duplicate_schema,
    update_schema,
)
from apps.applydesk.services.documents.schema_publish import publish_schema
from apps.applydesk.services.documents.schema_version import (
    create_schema_version,
)
from apps.applydesk.services.documents.schema_versioning import (
    get_or_create_draft,
)


def test_create_schema(db):
    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version()

    print(schema.versions.values("status", "version", "data"))  # ty:ignore[unresolved-attribute]

    assert schema.name == "CV"
    assert schema.document_type == "cv"
    assert version is not None
    assert version.data == {"fields": []}


def test_update_schema(db):
    schema = create_schema(
        name="Old",
        document_type="cv",
    )

    update_schema(
        schema=schema,
        name="New",
        document_type="cover_letter",
    )

    schema.refresh_from_db()

    assert schema.name == "New"
    assert schema.document_type == "cover_letter"


def test_duplicate_schema(db):
    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    # Draft Version anlegen
    draft = schema.draft_version()

    draft.data = {
        "fields": [
            {
                "name": "title",
                "label": "Title",
                "type": "text",
            }
        ]
    }
    draft.save()

    duplicate = duplicate_schema(schema=schema)
    print(duplicate.draft_version().data)
    dup_draft = duplicate.draft_version()
    print(f"Draft Data{dup_draft.data}")
    assert dup_draft is not None
    assert dup_draft.data == draft.data


def test_duplicate_schema_does_not_share_reference(db):
    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    draft = schema.draft_version()
    draft.data = {"fields": [{"name": "a"}]}
    draft.save()

    duplicate = duplicate_schema(schema=schema)

    dup_draft = duplicate.draft_version()

    # Mutation darf NICHT shared sein
    dup_draft.data["fields"].append({"name": "b"})
    dup_draft.save()

    original_draft = schema.draft_version()

    assert len(original_draft.data["fields"]) == 1


def test_duplicate_schema_has_own_draft(db):
    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    duplicate = duplicate_schema(schema=schema)

    assert schema.pk != duplicate.pk

    assert duplicate.draft_version() is not None
    assert duplicate.draft_version().status == "draft"


def test_publish_schema(db):
    schema = create_schema(
        name="Resume",
        document_type="cv",
    )

    draft = schema.latest_version()

    draft.data = {
        "fields": [
            {
                "name": "title",
            }
        ]
    }

    draft.save()
    publish_schema(schema=schema)
    published = schema.latest_published_version()
    assert published.version == 1
    assert published.status == "published"

    new_draft = schema.latest_version()

    assert new_draft is not None
    assert new_draft.pk != draft.pk
