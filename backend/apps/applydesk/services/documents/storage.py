from pathlib import Path


def build_storage_filename(
    *,
    document_name,
    original_filename,
):

    extension = Path(original_filename).suffix

    return f"{document_name}{extension}"


def document_upload_path(instance, filename):

    stored_filename = build_storage_filename(
        document_name=instance.title,
        original_filename=filename,
    )

    return f"documents/{instance.document_type}/{stored_filename}"
