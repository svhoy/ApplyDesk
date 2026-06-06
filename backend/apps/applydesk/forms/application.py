from django import forms

from apps.applydesk.models import Application


class BaseApplicationForm(forms.ModelForm):
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
