
def validate_revision_cycle_days(value: int):
    if value <= 0:
        raise ValueError("The revision cycle days must be > 0.")
    return value
