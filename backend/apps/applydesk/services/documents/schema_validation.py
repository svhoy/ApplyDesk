from dataclasses import dataclass


@dataclass
class SchemaValidationError:
    code: str
    message: str
    field: str | None = None


def validate_schema(schema):

    errors = []

    errors.extend(validate_schema_metadata(schema))

    errors.extend(validate_schema_version(schema))

    errors.extend(validate_schema_fields(schema))

    return errors


def validate_schema_metadata(schema):

    errors = []

    if not schema.name:
        errors.append(
            SchemaValidationError(
                code="missing_name",
                message="Schema name is required.",
            )
        )

    if not schema.document_type:
        errors.append(
            SchemaValidationError(
                code="missing_document_type",
                message="Document type is required.",
            )
        )

    return errors


def validate_schema_version(schema):

    errors = []

    if not schema.draft_version:
        errors.append(
            SchemaValidationError(
                code="missing_draft",
                message="Schema has no draft version.",
            )
        )

    return errors


def validate_schema_fields(schema):

    version = schema.draft_version

    if not version:
        return []

    fields = version.data.get("fields", [])

    errors = []

    if not fields:
        errors.append(
            SchemaValidationError(
                code="missing_fields",
                message="Schema requires at least one field.",
            )
        )

        return errors

    errors.extend(validate_field_names(fields))

    errors.extend(validate_field_structure(fields))

    errors.extend(validate_field_types(fields))

    errors.extend(validate_field_ids(fields))

    return errors


def validate_field_structure(fields):

    errors = []

    for field in fields:
        if not field.get("name"):
            errors.append(
                SchemaValidationError(
                    code="missing_field_name", message="Every field requires a name."
                )
            )

        if not field.get("label"):
            errors.append(
                SchemaValidationError(
                    code="missing_field_label",
                    message="Every field requires a label.",
                    field=field.get("name"),
                )
            )

        if not field.get("type"):
            errors.append(
                SchemaValidationError(
                    code="missing_field_type",
                    message="Every field requires a type.",
                    field=field.get("name"),
                )
            )

    return errors


ALLOWED_FIELD_TYPES = {
    "text",
    "textarea",
    "number",
    "date",
    "select",
    "checkbox",
}


def validate_field_types(fields):

    errors = []

    for field in fields:
        field_type = field.get("type")

        if field_type not in ALLOWED_FIELD_TYPES:
            errors.append(
                SchemaValidationError(
                    code="invalid_field_type",
                    message=f"Invalid field type: {field_type}",
                    field=field.get("name"),
                )
            )

    return errors


def validate_field_names(fields):

    errors = []

    names = set()

    for field in fields:
        name = field.get("name")

        if not name:
            continue

        if name in names:
            errors.append(
                SchemaValidationError(
                    code="duplicate_field_name",
                    message=f"Duplicate field name: {name}",
                    field=name,
                )
            )

        names.add(name)

    return errors


def validate_field_ids(fields):

    errors = []

    ids = []

    for field in fields:
        field_id = field.get("id")

        if not field_id:
            continue

        if field_id in ids:
            errors.append(
                SchemaValidationError(
                    code="duplicate_field_id",
                    message="Duplicate field id.",
                )
            )

        ids.append(field_id)

    return errors
