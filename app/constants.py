CITIZENSHIP_STATUSES = [
    'US Citizen', 
    'Non-US Citizen',
]

MARITAL_CHOICES = [
    "Married",
    "Single",
    "Divorced",
]

PROGRAM_TYPES = [
    "Short-Term",
    "Long-Term",
]

PREFERRED_CURRENCY = [
    "$",
    "£",
    "€",
    "ILS",
]


def generate_currency(currency: str, extract_symbol: bool = True):
    try:
        currency_list = currency.split("-")
        if extract_symbol:
            currency_symbol = currency_list[1].strip()
            return currency_symbol
        else:
            currency_name = currency_list[0].strip()
            return currency_name
    except:
        return ""
    