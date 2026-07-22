from apps.applydesk.services.documents.schema import create_schema
from apps.applydesk.services.documents.schema_fields import append_field
from apps.applydesk.services.documents.schema_validation import validate_schema


def test_valid_schema_has_no_errors(db):

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

    version = schema.draft_version

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


def test_field_without_label_is_invalid(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="first_name",
        label="",
        field_type="text",
        required=True,
    )

    errors = validate_schema(schema)

    assert any(error.code == "missing_field_label" for error in errors)


def test_field_without_type_is_invalid(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="first_name",
        label="First Name",
        field_type="",
        required=True,
    )

    errors = validate_schema(schema)

    assert any(error.code == "missing_field_type" for error in errors)


def test_invalid_field_type_is_invalid(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="age",
        label="Age",
        field_type="banana",
        required=False,
    )

    errors = validate_schema(schema)

    assert any(error.code == "invalid_field_type" for error in errors)


def test_schema_without_draft_is_invalid(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    schema.versions.all().delete()  # ty:ignore[unresolved-attribute]

    errors = validate_schema(schema)

    assert any(error.code == "missing_draft" for error in errors)
