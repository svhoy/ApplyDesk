from apps.applydesk.services.documents.form_builder import (
    build_document_form,
)


def test_build_form_from_schema():

    schema = {
        "fields": [
            {
                "name": "main_text",
                "label": "Main Text",
                "type": "textarea",
            }
        ]
    }

    FormClass = build_document_form(
        schema,
    )

    form = FormClass()

    assert "main_text" in form.fields


def test_build_text_field():

    schema = {
        "fields": [
            {
                "name": "recipient_name",
                "label": "Recipient",
                "type": "text",
            }
        ]
    }

    FormClass = build_document_form(
        schema,
    )

    form = FormClass()

    assert "recipient_name" in form.fields


def test_build_textarea_field():

    schema = {
        "fields": [
            {
                "name": "main_text",
                "label": "Main Text",
                "type": "textarea",
            }
        ]
    }

    FormClass = build_document_form(
        schema,
    )

    form = FormClass()

    assert form.fields["main_text"].widget.__class__.__name__ == "Textarea"


def test_required_field():

    schema = {
        "fields": [
            {
                "name": "main_text",
                "label": "Main Text",
                "type": "textarea",
                "required": True,
            }
        ]
    }

    FormClass = build_document_form(
        schema,
    )

    form = FormClass()

    assert form.fields["main_text"].required is True


def test_initial_values_are_applied():

    schema = {
        "fields": [
            {
                "name": "main_text",
                "label": "Main Text",
                "type": "textarea",
            }
        ]
    }

    FormClass = build_document_form(
        schema,
        initial={
            "main_text": "Hello World",
        },
    )

    form = FormClass()

    assert form["main_text"].value() == "Hello World"


def test_unknown_field_type_is_ignored():

    schema = {
        "fields": [
            {
                "name": "foo",
                "type": "future_ai_field",
            }
        ]
    }

    FormClass = build_document_form(
        schema,
    )

    form = FormClass()

    assert "foo" not in form.fields
