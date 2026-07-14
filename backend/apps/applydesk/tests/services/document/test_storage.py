from apps.applydesk.services.documents.storage import (
    document_upload_path,
)


class DummyDocument:
    title = "cv_google"
    document_type = "cv"


class DummyCertificate:
    title = "certificate_google"
    document_type = "certificate_work"


def test_cv_upload_path():

    path = document_upload_path(
        DummyDocument(),
        "cv_google.pdf",
    )

    assert path == "documents/cv/cv_google.pdf"


def test_certificate_upload_path():

    path = document_upload_path(
        DummyCertificate(),
        "certificate_google.pdf",
    )

    assert path == "documents/certificate_work/certificate_google.pdf"
