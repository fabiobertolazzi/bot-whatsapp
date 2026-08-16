def format_currency(value) -> str:
    if value is None or value == "":
        return "R$ 0,00"

    if isinstance(value, str):
        value = (
            value
            .replace("R$", "")
            .replace(" ", "")
            .replace(".", "")
            .replace(",", ".")
        )

    value = float(value)

    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")