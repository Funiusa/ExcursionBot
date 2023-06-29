import phonenumbers


def phone_validation(phone) -> bool:
    phone = phone if phone[0] == "+" else "+" + phone
    try:
        phone = phonenumbers.parse(phone)
        return phonenumbers.is_valid_number(phone)
    except phonenumbers.NumberParseException:
        return False
