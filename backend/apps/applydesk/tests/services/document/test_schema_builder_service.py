from apps.applydesk.services.documents.schema_builder import (
    add_field,
    remove_field,
    reorder_fields,
)


def test_add_field_to_schema():

    schema = {"fields": []}

    updated = add_field(
        schema,
        {
            "name": "main_text",
            "type": "textarea",
            "label": "Main Text",
        },
    )

    assert len(updated["fields"]) == 1


def test_remove_field_from_schema():

    schema = {"fields": [{"name": "main_text", "type": "textarea"}]}

    updated = remove_field(schema, "main_text")

    assert updated["fields"] == []


def test_reorder_fields():

    schema = {
        "fields": [
            {"name": "a", "type": "text"},
            {"name": "b", "type": "text"},
        ]
    }

    updated = reorder_fields(schema, ["b", "a"])

    assert updated["fields"][0]["name"] == "b"
