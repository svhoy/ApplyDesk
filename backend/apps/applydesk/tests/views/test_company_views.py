import pytest
from django.urls import reverse

from apps.applydesk.models import Application

# -------------------------
# LIST VIEW
# -------------------------


@pytest.mark.django_db
def test_company_list_view(client):

    response = client.get(reverse("company_list"))

    assert response.status_code == 200


# -------------------------
# DETAIL VIEW (CORE)
# -------------------------


@pytest.mark.django_db
def test_company_detail_view(client, company):

    response = client.get(reverse("company_detail", args=[company.pk]))

    assert response.status_code == 200
    assert company.name in response.content.decode()


@pytest.mark.django_db
def test_company_detail_empty_state(client, company):

    response = client.get(reverse("company_detail", args=[company.pk]))

    content = response.content.decode()

    assert "Backend Engineer" not in content


# -------------------------
# DETAIL: SHOW APPLICATIONS
# -------------------------


@pytest.mark.django_db
def test_company_detail_shows_applications(client, company):

    Application.objects.create(
        company=company,
        position_title="Backend Engineer",
    )

    response = client.get(reverse("company_detail", args=[company.pk]))

    content = response.content.decode()

    assert "Backend Engineer" in content


# -------------------------
# DETAIL: STATISTICS
# -------------------------


@pytest.mark.django_db
def test_company_detail_statistics(client, company):

    Application.objects.create(
        company=company,
        position_title="Backend",
    )

    Application.objects.create(
        company=company,
        position_title="DevOps",
    )

    response = client.get(reverse("company_detail", args=[company.pk]))

    content = response.content.decode()

    # robust statt "magic string"
    assert "2" in content


# -------------------------
# CREATE
# -------------------------


@pytest.mark.django_db
def test_company_create_view(client):

    response = client.post(
        reverse("company_create"),
        {"name": "Google"},
    )

    assert response.status_code == 302


# -------------------------
# EDIT
# -------------------------


@pytest.mark.django_db
def test_company_edit_view(client, company):

    response = client.post(
        reverse("company_edit", args=[company.pk]),
        {"name": "Google DE"},
    )

    assert response.status_code == 302

    company.refresh_from_db()
    assert company.name == "Google DE"


# -------------------------
# EDIT
# -------------------------
@pytest.mark.django_db
def test_company_delete_success(client, company):

    response = client.post(reverse("company_delete", args=[company.pk]))

    assert response.status_code == 302
    assert not company.__class__.objects.filter(pk=company.pk).exists()
