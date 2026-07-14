from django import forms

from apps.applydesk.models import Application
from apps.applydesk.models.document import DocumentType


class BaseApplicationForm(forms.ModelForm):
    required_documents = forms.MultipleChoiceField(
        choices=DocumentType.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if instance:
            self.fields["required_documents"].initial = list(
                instance.required_documents.values_list(
                    "document_type",
                    flat=True,
                )
            )

    class Meta:
        model = Application

        fields = [
            "position_title",
            "position_description",
            "location",
            "location_type",
            "notes",
            "url",
            "start_date",
            "contact_person",
            "contact_email",
            "contact_phone",
        ]


class ApplicationForm(BaseApplicationForm):
    company_name = forms.CharField(max_length=200)


class ApplicationUpdateForm(
    BaseApplicationForm,
):
    pass
