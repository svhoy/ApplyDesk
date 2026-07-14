WORKFLOW_ACTIONS = {
    "saved": [
        {
            "to": "prepared",
            "label": "Mark as Prepared",
            "color": "green",
        },
        {
            "to": "pre_screen",
            "label": "Pre-Screen",
            "color": "blue",
        },
        {
            "to": "closed",
            "label": "Position Closed",
            "color": "red",
        },
    ],
    "prepared": [
        {
            "to": "applied",
            "label": "Mark as Applied",
            "color": "green",
        },
        {
            "to": "closed",
            "label": "Position Closed",
            "color": "red",
        },
    ],
    "applied": [
        {
            "to": "waiting",
            "label": "Move to Waiting",
            "color": "gray",
        },
        {
            "to": "interview",
            "label": "Interview",
            "color": "green",
        },
        {
            "to": "rejected",
            "label": "Reject",
            "color": "red",
        },
        {
            "to": "closed",
            "label": "Position Closed",
            "color": "red",
        },
    ],
    "waiting": [
        {
            "to": "interview",
            "label": "Interview",
            "color": "green",
        },
        {
            "to": "rejected",
            "label": "Reject",
            "color": "red",
        },
        {
            "to": "closed",
            "label": "Position Closed",
            "color": "red",
        },
    ],
    "interview": [
        {
            "to": "offer",
            "label": "Offer",
            "color": "green",
        },
        {
            "to": "rejected",
            "label": "Reject",
            "color": "red",
        },
        {
            "to": "closed",
            "label": "Position Closed",
            "color": "red",
        },
    ],
    "offer": [
        {
            "to": "archived",
            "label": "Archive",
            "color": "gray",
        }
    ],
    "rejected": [
        {
            "to": "archived",
            "label": "Archive",
            "color": "gray",
        }
    ],
    "closed": [
        {
            "to": "archived",
            "label": "Archive",
            "color": "gray",
        }
    ],
}


def get_available_actions(application):

    actions = list(
        WORKFLOW_ACTIONS.get(
            application.status,
            [],
        )
    )

    if application.status == "saved":
        has_contact = bool(application.contact_email or application.contact_phone)

        if not has_contact:
            actions = [action for action in actions if action["to"] != "pre_screen"]

    return actions
