import re

from apps.applydesk.models import Document


def normalize_name(value: str) -> str:

    value = value.strip().lower()

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value,
    )

    return value.strip("_")


def build_document_base_name(
    *,
    document_type: str,
    company_name: str,
) -> str:

    return f"{document_type}_{normalize_name(company_name)}"


def get_next_versioned_name(
    *,
    base_name: str,
) -> str:

    existing_titles = set(
        Document.objects.filter(
            title__startswith=base_name,
        ).values_list(
            "title",
            flat=True,
        )
    )

    if base_name not in existing_titles:
        return base_name

    version = 2

    while True:
        candidate = f"{base_name}_v{version}"

        if candidate not in existing_titles:
            return candidate

        version += 1
