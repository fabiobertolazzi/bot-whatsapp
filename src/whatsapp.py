import requests

from src.secrets import get_meta_token, get_phone_number_id

WHATSAPP_API_VERSION = "v22.0"
WHATSAPP_BASE_URL = "https://graph.facebook.com"


def send_whatsapp(phone: str, message: str) -> dict:
    """
    Envia uma mensagem de texto via WhatsApp Business API.

    Args:
        phone:   Número no formato internacional sem '+' (ex: 5511999999999).
        message: Texto da mensagem.

    Retorno:
        Dicionário com status_code e body da resposta.

    Raises:
        Exception: Se a API retornar status diferente de 200.
    """
    token = get_meta_token()
    phone_number_id = get_phone_number_id()

    url = f"{WHATSAPP_BASE_URL}/{WHATSAPP_API_VERSION}/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(url, headers=headers, json=payload)

    print(f"[WhatsApp] para={phone} | status={response.status_code}")

    if response.status_code != 200:
        raise Exception(f"Erro WhatsApp API: {response.text}")

    return {"status_code": response.status_code, "body": response.text}
