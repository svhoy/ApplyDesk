from dataclasses import dataclass


@dataclass
class SchemaValidationError:
    code: str
    message: str


def validate_schema(schema):
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

    version = schema.draft_version()

    if not version:
        errors.append(
            SchemaValidationError(
                code="missing_draft",
                message="Schema has no draft version.",
            )
        )

        return errors

    fields = version.data.get(
        "fields",
        [],
    )

    if not fields:
        errors.append(
            SchemaValidationError(
                code="missing_fields",
                message="Schema requires at least one field.",
            )
        )

    errors.extend(validate_field_names(fields))

    return errors


def validate_field_names(fields):

    errors = []

    names = []

    for field in fields:
        name = field.get("name")

        if not name:
            errors.append(
                SchemaValidationError(
                    code="missing_field_name",
                    message="Every field requires a name.",
                )
            )

            continue

        if name in names:
            errors.append(
                SchemaValidationError(
                    code="duplicate_field_name",
                    message=f"Duplicate field name: {name}",
                )
            )

        names.append(name)

    return errors
