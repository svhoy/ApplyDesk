from apps.applydesk.models.application import ApplicationRequiredDocument


def sync_required_documents(application, required_docs: list[str]):

    application.required_documents.all().delete()

    ApplicationRequiredDocument.objects.bulk_create(
        [
            ApplicationRequiredDocument(
                application=application,
                document_type=doc_type,
            )
            for doc_type in required_docs
        ]
    )
