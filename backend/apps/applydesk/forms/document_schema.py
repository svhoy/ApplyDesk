from django import forms

from apps.applydesk.models import DocumentSchema
from apps.applydesk.models.document import DocumentType

FIELD_TYPE_CHOICES = (
    ("text", "Text"),
    ("textarea", "Textarea"),
    ("date", "Date"),
    ("number", "Number"),
    ("email", "Email"),
    ("boolean", "Checkbox"),
)


class DocumentSchemaGeneralForm(forms.ModelForm):
    document_type = forms.ChoiceField(choices=DocumentType.choices)

    class Meta:
        model = DocumentSchema
        fields = ["name", "document_type"]


class DocumentSchemaFieldForm(forms.Form):
    name = forms.CharField(max_length=100)

    label = forms.CharField(max_length=100)

    field_type = forms.ChoiceField(
        choices=FIELD_TYPE_CHOICES,
    )

    required = forms.BooleanField(
        required=False,
    )
