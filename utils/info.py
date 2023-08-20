from . import messages


def _request_info():
    last_name = input(f"{messages.INPUT_LAST_NAME}")
    first_name = input(f"{messages.INPUT_FIRST_NAME}")
    middle_name = input(f"{messages.INPUT_MIDDLE_NAME}")
    organization = input(f"{messages.INPUT_ORGANIZATION}")
    work_phone = input(f"{messages.INPUT_WORK_PHONE}")
    personal_phone = input(f"{messages.INPUT_PERSONAL_PHONE}")

    note = {
        "last_name": last_name,
        "first_name": first_name,
        "middle_name": middle_name,
        "organization": organization,
        "work_phone": work_phone,
        "personal_phone": personal_phone,
    }
    return note
