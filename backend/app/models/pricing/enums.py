import enum

class DiscountType(enum.Enum):
    # Enum is used instead of string to avoid invalid values like "percent" or "PERC"
    PERCENTAGE = "PERCENTAGE"
    AMOUNT = "AMOUNT"
