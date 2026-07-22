from apps.applydesk.services.documents.schema import create_schema
from apps.applydesk.services.documents.schema_fields import (
    append_field,
    delete_field,
    get_field,
    move_field,
    update_field,
)


def test_append_field(db):
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

    fields = version.data["fields"]

    assert len(fields) == 1

    assert fields[0]["name"] == "first_name"
    assert fields[0]["label"] == "First Name"
    assert fields[0]["type"] == "text"
    assert fields[0]["required"] is True
    assert "id" in fields[0]


def test_get_field(db):
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

    field_id = version.data["fields"][0]["id"]

    field = get_field(
        version,
        field_id,
    )

    assert field is not None
    assert field["id"] == field_id
    assert field["name"] == "first_name"


def test_update_field(db):
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

    field_id = version.data["fields"][0]["id"]

    update_field(
        version,
        field_id=field_id,
        label="Given Name",
        required=False,
    )

    field = get_field(
        version,
        field_id,
    )

    assert field["label"] == "Given Name"
    assert field["required"] is False
    assert field["name"] == "first_name"


def test_delete_field(db):
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

    append_field(
        version,
        name="last_name",
        label="Last Name",
        field_type="text",
        required=True,
    )

    field_id = version.data["fields"][0]["id"]

    delete_field(
        version,
        field_id=field_id,
    )

    fields = version.data["fields"]

    assert len(fields) == 1
    assert fields[0]["name"] == "last_name"


def test_move_field_forward(db):
    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="first",
        label="First",
        field_type="text",
        required=True,
    )

    append_field(
        version,
        name="second",
        label="Second",
        field_type="text",
        required=True,
    )

    field_id = version.data["fields"][0]["id"]

    move_field(
        version,
        field_id=field_id,
        new_index=1,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "second"
    assert fields[1]["name"] == "first"


def test_move_field_backward(db):
    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="first",
        label="First",
        field_type="text",
        required=True,
    )

    append_field(
        version,
        name="second",
        label="Second",
        field_type="text",
        required=True,
    )

    field_id = version.data["fields"][1]["id"]

    move_field(
        version,
        field_id=field_id,
        new_index=0,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "second"
    assert fields[1]["name"] == "first"


def test_update_field_preserves_other_fields(db):
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

    append_field(
        version,
        name="last_name",
        label="Last Name",
        field_type="text",
        required=False,
    )

    first_field_id = version.data["fields"][0]["id"]

    update_field(
        version,
        field_id=first_field_id,
        label="Given Name",
    )

    fields = version.data["fields"]

    assert len(fields) == 2

    assert fields[0]["label"] == "Given Name"
    assert fields[0]["name"] == "first_name"

    # Zweites Feld darf komplett unverändert bleiben
    assert fields[1]["name"] == "last_name"
    assert fields[1]["label"] == "Last Name"
    assert fields[1]["required"] is False


def test_add_field_persists_on_draft_version(db):
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

    version.refresh_from_db()

    assert version.data["fields"][0]["name"] == "first_name"


def test_update_field_changes_existing_field(db):
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

    field_id = version.data["fields"][0]["id"]

    update_field(
        version,
        field_id=field_id,
        label="Given Name",
    )

    field = get_field(
        version,
        field_id,
    )

    assert field["label"] == "Given Name"
    assert field["name"] == "first_name"


def test_delete_field_removes_field(db):
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

    field_id = version.data["fields"][0]["id"]

    delete_field(
        version,
        field_id=field_id,
    )

    assert version.data["fields"] == []


def create_schema_with_fields():
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

    append_field(
        version,
        name="last_name",
        label="Last Name",
        field_type="text",
        required=True,
    )

    append_field(
        version,
        name="email",
        label="Email",
        field_type="text",
        required=False,
    )

    return schema, version


def test_move_field_down(db):
    schema, version = create_schema_with_fields()

    first_field_id = version.data["fields"][0]["id"]

    move_field(
        version,
        field_id=first_field_id,
        new_index=1,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "last_name"
    assert fields[1]["name"] == "first_name"
    assert fields[2]["name"] == "email"


def test_move_field_up(db):
    schema, version = create_schema_with_fields()

    last_field_id = version.data["fields"][2]["id"]

    move_field(
        version,
        field_id=last_field_id,
        new_index=1,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "first_name"
    assert fields[1]["name"] == "email"
    assert fields[2]["name"] == "last_name"


def test_move_field_to_first_position(db):
    schema, version = create_schema_with_fields()

    last_field_id = version.data["fields"][2]["id"]

    move_field(
        version,
        field_id=last_field_id,
        new_index=0,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "email"
    assert fields[1]["name"] == "first_name"
    assert fields[2]["name"] == "last_name"


def test_move_field_to_last_position(db):
    schema, version = create_schema_with_fields()

    first_field_id = version.data["fields"][0]["id"]

    move_field(
        version,
        field_id=first_field_id,
        new_index=2,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "last_name"
    assert fields[1]["name"] == "email"
    assert fields[2]["name"] == "first_name"


def test_move_field_keeps_other_field_data(db):
    schema, version = create_schema_with_fields()

    first_field_id = version.data["fields"][0]["id"]

    move_field(
        version,
        field_id=first_field_id,
        new_index=2,
    )

    moved_field = version.data["fields"][2]

    assert moved_field["name"] == "first_name"
    assert moved_field["label"] == "First Name"
    assert moved_field["type"] == "text"
    assert moved_field["required"] is True


def test_move_field_invalid_id_does_nothing(db):
    schema, version = create_schema_with_fields()

    original = version.data["fields"].copy()

    move_field(
        version,
        field_id="does-not-exist",
        new_index=1,
    )

    assert version.data["fields"] == original


def test_move_field_index_too_low_moves_to_first_position(db):
    schema, version = create_schema_with_fields()

    email_id = version.data["fields"][2]["id"]

    move_field(
        version,
        field_id=email_id,
        new_index=-10,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "email"


def test_move_field_index_too_high_moves_to_last_position(db):
    schema, version = create_schema_with_fields()

    first_field_id = version.data["fields"][0]["id"]

    move_field(
        version,
        field_id=first_field_id,
        new_index=999,
    )

    fields = version.data["fields"]

    assert fields[-1]["name"] == "first_name"


def test_update_field_ignores_unknown_values(db):

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

    field_id = version.data["fields"][0]["id"]

    update_field(
        version,
        field_id=field_id,
        label="Changed",
        hacker_value="test",
    )

    field = get_field(
        version,
        field_id,
    )

    assert field["label"] == "Changed"

    assert "hacker_value" not in field


def test_append_field_sets_position(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    version = schema.draft_version

    append_field(
        version,
        name="first",
        label="First",
        field_type="text",
        required=False,
    )

    assert version.data["fields"][0]["position"] == 0


def test_move_field_updates_positions(db):

    schema, version = create_schema_with_fields()

    first_field_id = version.data["fields"][0]["id"]

    move_field(
        version,
        field_id=first_field_id,
        new_index=2,
    )

    fields = version.data["fields"]

    assert fields[0]["position"] == 0
    assert fields[1]["position"] == 1
    assert fields[2]["position"] == 2


def test_delete_field_updates_positions(db):

    schema, version = create_schema_with_fields()

    first_field_id = version.data["fields"][0]["id"]

    delete_field(
        version,
        field_id=first_field_id,
    )

    fields = version.data["fields"]

    assert fields[0]["name"] == "last_name"

    assert fields[0]["position"] == 0
    assert fields[1]["position"] == 1


def test_append_field_creates_field(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    draft = schema.draft_version

    append_field(
        draft,
        name="first_name",
        label="First Name",
        field_type="text",
        required=True,
    )

    fields = draft.data["fields"]

    assert len(fields) == 1

    assert fields[0]["name"] == "first_name"

    assert fields[0]["required"] is True


def test_update_field_changes_field(db):

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
        required=False,
    )

    field_id = draft.data["fields"][0]["id"]

    update_field(
        draft,
        field_id=field_id,
        label="Full Name",
    )

    assert draft.data["fields"][0]["label"] == "Full Name"


def test_delete_field_removes_field(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    draft = schema.draft_version

    append_field(
        draft,
        name="email",
        label="Email",
        field_type="text",
        required=False,
    )

    field_id = draft.data["fields"][0]["id"]

    delete_field(
        draft,
        field_id=field_id,
    )

    assert draft.data["fields"] == []


def test_move_field_changes_order(db):

    schema = create_schema(
        name="CV",
        document_type="cv",
    )

    draft = schema.draft_version

    append_field(
        draft,
        name="first",
        label="First",
        field_type="text",
        required=False,
    )

    append_field(
        draft,
        name="second",
        label="Second",
        field_type="text",
        required=False,
    )

    second_id = draft.data["fields"][1]["id"]

    move_field(
        draft,
        field_id=second_id,
        new_index=0,
    )

    assert draft.data["fields"][0]["name"] == "second"
