from apps.applydesk.models.versioned import VersionStatus
from apps.applydesk.services.documents.schema import create_schema
from apps.applydesk.services.documents.schema_fields import append_field
from apps.applydesk.services.documents.schema_publish import publish_schema


def test_publish_schema_creates_new_draft(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="first_name",
        label="First Name",
        field_type="text",
        required=True,
    )

    result = publish_schema(
        schema=schema,
    )

    assert result["success"] is True

    schema.refresh_from_db()

    published = schema.latest_published_version
    draft = schema.draft_version

    assert published.status == VersionStatus.PUBLISHED
    assert draft.status == VersionStatus.DRAFT

    assert published.version == 1
    assert draft.version == 2

    assert published.data == draft.data


def test_publish_schema_without_fields_fails(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    result = publish_schema(
        schema=schema,
    )

    assert result["success"] is False

    assert any(error.code == "missing_fields" for error in result["errors"])


def test_publish_does_not_delete_old_version(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="email",
        label="Email",
        field_type="text",
        required=False,
    )

    publish_schema(
        schema=schema,
    )

    assert schema.versions.count() == 2  # ty:ignore[unresolved-attribute]
