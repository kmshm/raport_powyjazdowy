"""
Field validation utilities.
"""
from datetime import date


def validate_required_fields(data: dict) -> list[str]:
    """
    Validate that all required fields are present and non-empty.
    Returns a list of human-readable error messages (empty = all OK).
    """
    errors = []

    initials = (data.get("initials") or "").strip()
    if not initials:
        errors.append("Inicjały wypełniającego są wymagane.")

    project_number = (data.get("project_number") or "").strip()
    if not project_number:
        errors.append("Numer projektu jest wymagany.")

    measurement_dates = data.get("measurement_dates") or []
    if not measurement_dates:
        errors.append("Data pomiarów jest wymagana.")

    return errors


def build_filename(data: dict) -> str:
    """
    Build the PDF filename: YYYY-MM-DD-{project_number}-{initials}
    Uses the first measurement date. Falls back to today if no date given.
    """
    dates = data.get("measurement_dates") or []
    if dates:
        first = dates[0]
        if isinstance(first, date):
            date_str = first.strftime("%Y-%m-%d")
        else:
            date_str = str(first)
    else:
        date_str = date.today().strftime("%Y-%m-%d")

    project_number = (data.get("project_number") or "BRAK").strip()
    initials = (data.get("initials") or "XX").strip()

    # Replace spaces and slashes to keep filename filesystem-safe
    project_number = project_number.replace(" ", "_").replace("/", "-")
    initials = initials.replace(" ", "_")

    return f"{date_str}-{project_number}-{initials}.pdf"
