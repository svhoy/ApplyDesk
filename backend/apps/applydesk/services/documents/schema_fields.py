from copy import deepcopy
from uuid import uuid4

ALLOWED_FIELD_ATTRIBUTES = {
    "name",
    "label",
    "type",
    "required",
}


# private helper
def save_schema_data(version, data):
    version.data = data
    version.save(update_fields=["data"])
    return version


def normalize_fields(fields):

    for index, field in enumerate(fields):
        field["position"] = index

    return fields


def _get_fields(version):

    data = deepcopy(version.data or {})

    if "fields" not in data:
        data["fields"] = []

    normalize_fields(data["fields"])

    return data


# public API
def append_field(
    version,
    *,
    name,
    label,
    field_type,
    required,
):
    data = _get_fields(version)

    data["fields"].append(
        {
            "id": str(uuid4()),
            "name": name,
            "label": label,
            "type": field_type,
            "required": required,
        }
    )

    normalize_fields(data["fields"])

    return save_schema_data(
        version,
        data,
    )


def get_field(version, field_id):
    for field in version.data.get("fields", []):
        if field["id"] == field_id:
            return field

    return None


def update_field(
    version,
    *,
    field_id,
    **changes,
):
    data = _get_fields(version)

    for field in data["fields"]:
        if field["id"] == field_id:
            field.update(
                {
                    key: value
                    for key, value in changes.items()
                    if key in ALLOWED_FIELD_ATTRIBUTES
                }
            )
            break

    return save_schema_data(
        version,
        data,
    )


def delete_field(
    version,
    *,
    field_id,
):
    data = _get_fields(version)

    data["fields"] = [field for field in data["fields"] if field["id"] != field_id]
    normalize_fields(data["fields"])
    return save_schema_data(
        version,
        data,
    )


def move_field(
    version,
    *,
    field_id,
    new_index,
):
    data = _get_fields(version)

    fields = data["fields"]

    current_index = next(
        (index for index, field in enumerate(fields) if field["id"] == field_id),
        None,
    )

    if current_index is None:
        return version

    field = fields.pop(current_index)

    new_index = max(
        0,
        min(new_index, len(fields)),
    )

    fields.insert(
        new_index,
        field,
    )
    normalize_fields(fields)
    return save_schema_data(
        version,
        data,
    )
