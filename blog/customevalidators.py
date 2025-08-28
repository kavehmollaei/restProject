from django.core.exceptions import ValidationError

def validate_11_digit_phone(value):
    # Convert to string to count digits
    str_value = str(value)
    if len(str_value) != 11:
        raise ValidationError(
            f"{value} must be exactly 11 digits.",
            code="invalid_phone_length"
        )