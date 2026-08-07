import json
import os
import boto3

from src.config import SECRET_NAME, REGION_NAME


def get_secret() -> dict:
    """
    Busca e retorna o segredo completo do Secrets Manager como dicionário.
    Em ambiente local, pode ser sobrescrito por variáveis de ambiente.
    """
    # ── Modo local: usa variáveis de ambiente em vez da AWS ──────────────────
    if os.getenv("LOCAL_MODE") == "true":
        return _get_secret_from_env()

    client = boto3.client("secretsmanager", region_name=REGION_NAME)
    response = client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(response["SecretString"])


def get_meta_token() -> str:
    return get_secret()["meta_token"]


def get_phone_number_id() -> str:
    return get_secret()["phone_number_id"]


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_secret_from_env() -> dict:
    """
    Constrói o dicionário de segredos a partir de variáveis de ambiente locais.
    Útil para rodar e testar sem conexão com a AWS.
    """
    required = [
        "meta_token",
        "phone_number_id",
        "type",
        "project_id",
        "private_key_id",
        "private_key",
        "client_email",
        "client_id",
        "auth_uri",
        "token_uri",
        "auth_provider_x509_cert_url",
        "client_x509_cert_url",
    ]

    secret = {}
    missing = []

    for key in required:
        value = os.getenv(key.upper())
        if value is None:
            missing.append(key.upper())
        else:
            secret[key] = value

    if missing:
        raise EnvironmentError(
            f"LOCAL_MODE=true mas as seguintes variáveis não foram definidas: "
            f"{', '.join(missing)}\n"
            f"Configure o arquivo .env antes de rodar localmente."
        )

    return secret
