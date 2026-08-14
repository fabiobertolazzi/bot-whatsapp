def format_currency(value) -> str:
    if value is None or value == "":
        return "R$ 0,00"

    value = float(value)

    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")