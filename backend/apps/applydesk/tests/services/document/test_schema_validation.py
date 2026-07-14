from apps.applydesk.services.documents.schema import create_schema
from apps.applydesk.services.documents.schema_fields import append_field
from apps.applydesk.services.documents.schema_validation import validate_schema


def test_valid_schema_has_no_errors(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version()

    append_field(
        version,
        name="first_name",
        label="First Name",
        field_type="text",
        required=True,
    )

    errors = validate_schema(schema)

    assert errors == []


def test_schema_without_name_is_invalid(db):

    schema = create_schema(
        name="",
        document_type="cv",
    )

    errors = validate_schema(schema)

    assert any(error.code == "missing_name" for error in errors)


def test_schema_without_fields_is_invalid(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    errors = validate_schema(schema)

    assert any(error.code == "missing_fields" for error in errors)


def test_duplicate_field_names_are_invalid(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version()

    append_field(
        version,
        name="email",
        label="Email",
        field_type="text",
        required=False,
    )

    append_field(
        version,
        name="email",
        label="Email 2",
        field_type="text",
        required=False,
    )

    errors = validate_schema(schema)

    assert any(error.code == "duplicate_field_name" for error in errors)
