def format_duration(seconds: float) -> str:

    minutes = seconds / 60
    hours = seconds / 3600
    days = seconds / 86400

    if seconds < 60:
        return f"{seconds:.0f}s"

    if minutes < 60:
        return f"{minutes:.1f}m"

    if hours < 24:
        return f"{hours:.1f}h"

    return f"{days:.1f}d"
