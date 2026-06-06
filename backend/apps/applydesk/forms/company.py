from django import forms

from apps.applydesk.models import Company


class BaseCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "street",
            "street_number",
            "city",
            "zipcode",
            "country",
            "url",
            "career_site",
        ]


class CompanyCreateForm(
    BaseCompanyForm,
):
    pass


class CompanyUpdateForm(
    BaseCompanyForm,
):
    pass
