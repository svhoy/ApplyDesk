from django.shortcuts import get_object_or_404, redirect, render

from apps.applydesk.forms.company import (
    CompanyCreateForm,
    CompanyUpdateForm,
)
from apps.applydesk.models import Company
from apps.applydesk.queries.companies import get_company, list_companies
from apps.applydesk.services.companies.create import create_company
from apps.applydesk.services.companies.delete import delete_company
from apps.applydesk.services.companies.update import update_company


def company_list(request):

    companies = list_companies()

    return render(
        request,
        "companies/list.html",
        {
            "companies": companies,
        },
    )


def company_detail(
    request,
    company_id,
):
    company = get_company(
        company_id,
    )

    return render(
        request,
        "companies/detail.html",
        {
            "company": company,
        },
    )


def company_create(request):

    if request.method == "POST":
        form = CompanyCreateForm(request.POST)

        if form.is_valid():
            company = create_company(**form.cleaned_data)
            return redirect("company_detail", company.pk)

    else:
        form = CompanyCreateForm()

    return render(
        request,
        "companies/form.html",
        {"form": form, "mode": "create"},
    )


def company_edit(request, company_id):

    company = get_object_or_404(Company, pk=company_id)

    if request.method == "POST":
        form = CompanyUpdateForm(request.POST, instance=company)

        if form.is_valid():
            update_company(company, **form.cleaned_data)
            return redirect("company_detail", company.pk)

    else:
        form = CompanyUpdateForm(instance=company)

    return render(
        request,
        "companies/form.html",
        {"form": form, "mode": "edit", "company": company},
    )


def company_delete(request, company_id):

    company = get_object_or_404(Company, pk=company_id)

    if request.method == "POST":
        delete_company(company)
        return redirect("company_list")

    return render(
        request,
        "companies/confirm_delete.html",
        {"company": company},
    )
