def format_currency(value) -> str:
    """Formata um valor numérico ou string para o formato brasileiro de moeda (R$ 1.234,56).

    Suporta entradas numéricas (int/float) e strings em vários formatos, por exemplo:
    - "1646,11"  -> 1646.11
    - "1.646,11" -> 1646.11
    - "1646.11"  -> 1646.11
    - "R$ 1.646,11" -> 1646.11
    Em caso de entrada inválida retorna "R$ 0,00".
    """
    if value is None or value == "":
        return "R$ 0,00"

    # Normalizar tipos numéricos diretamente
    if isinstance(value, (int, float)):
        num = float(value)
    else:
        s = str(value).strip()
        # remover símbolo de moeda e espaços extras
        s = s.replace("R$", "").replace("$", "").strip()

        # Se contém ambos '.' e ',' é provável que '.' seja separador de milhar e ',' decimal
        if "." in s and "," in s:
            s = s.replace('.', '').replace(',', '.')
        else:
            # Se contém apenas vírgula, tratá-la como separador decimal
            if "," in s and "." not in s:
                s = s.replace(',', '.')
            # Se contém apenas ponto, assume-se que já é formato com ponto decimal
            # Caso contenha caracteres não numéricos, tentar extrair o trecho relevante
        try:
            num = float(s)
        except ValueError:
            import re
            m = re.search(r'-?[\d\.\,]+', s)
            if not m:
                return "R$ 0,00"
            s2 = m.group(0)
            if "." in s2 and "," in s2:
                s2 = s2.replace('.', '').replace(',', '.')
            elif "," in s2:
                s2 = s2.replace(',', '.')
            try:
                num = float(s2)
            except Exception:
                return "R$ 0,00"

    # Formatar com separador de milhar '.' e decimal ',' (padrão brasileiro)
    formatted = f"{num:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"
