from apps.applydesk.services.documents.schema import create_schema
from apps.applydesk.services.documents.schema_fields import append_field
from apps.applydesk.services.documents.schema_publish import publish_schema


def test_complete_schema_flow(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    draft = schema.draft_version

    append_field(
        draft,
        name="name",
        label="Name",
        field_type="text",
        required=True,
    )

    result = publish_schema(
        schema=schema,
    )

    assert result["success"] is True

    schema.refresh_from_db()

    assert schema.latest_published_version is not None

    assert schema.latest_published_version.data["fields"][0]["name"] == "name"
