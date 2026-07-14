import pytest

from apps.applydesk.services.applications.documents import sync_required_documents


@pytest.mark.django_db
def test_sync_required_documents_sets_documents(application):

    sync_required_documents(
        application,
        ["cv", "cover_letter"],
    )

    assert set(
        application.required_documents.values_list(
            "document_type",
            flat=True,
        )
    ) == {"cv", "cover_letter"}

@pytest.mark.django_db
def test_sync_required_documents_overwrites_existing(application):

    sync_required_documents(
        application,
        ["cv"],
    )

    sync_required_documents(
        application,
        ["cover_letter"],
    )

    assert set(
        application.required_documents.values_list(
            "document_type",
            flat=True,
        )
    ) == {"cover_letter"}

@pytest.mark.django_db
def test_sync_required_documents_empty_clears(application):

    sync_required_documents(
        application,
        ["cv"],
    )

    sync_required_documents(application, [])

    assert application.required_documents.count() == 0
