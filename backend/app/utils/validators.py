def validate_amount(value):
    try:
        v = float(value)
        if v <= 0:
            return None, "Amount must be positive"
        return v, None
    except (TypeError, ValueError):
        return None, "Amount must be a number"


def validate_date(value):
    if not value:
        return None, "Date is required"
    import re
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
        return None, "Date must be YYYY-MM-DD"
    return value, None


def validate_payment_method(value):
    allowed = ['Cash', 'GPay', 'Credit Card', 'Debit Card', 'Wallet']
    if value not in allowed:
        return None, f"Payment method must be one of: {', '.join(allowed)}"
    return value, None
