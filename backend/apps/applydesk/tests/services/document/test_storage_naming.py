from apps.applydesk.services.documents.storage import (
    build_storage_filename,
)


def test_storage_filename_keeps_extension():

    result = build_storage_filename(
        document_name="cv_google",
        original_filename="resume.pdf",
    )

    assert result == "cv_google.pdf"


def test_storage_filename_handles_docx():

    result = build_storage_filename(
        document_name="cv_google_v2",
        original_filename="resume.docx",
    )

    assert result == "cv_google_v2.docx"
