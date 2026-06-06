from apps.applydesk.models import Application


def delete_application(application: Application):
    application.delete()
