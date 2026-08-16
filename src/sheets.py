import gspread

from google.oauth2.service_account import Credentials

from src.config import (GOOGLE_SCOPES, SPREADSHEET_ID_MOTORA, SPREADSHEET_ID_FINAN)
from src.secrets import get_secret


def get_google_credentials() -> Credentials:
    """Constrói as credenciais do Google a partir do Secrets Manager."""

    credentials_info = get_secret()

    print(
        f"Google service account: "
        f"{credentials_info.get('client_email')}"
    )

    return Credentials.from_service_account_info(
        credentials_info,
        scopes=GOOGLE_SCOPES
    )

def get_sheet_records(spreadsheet_id: str, worksheet_name: str) -> list[dict]:
    """
    Abre a planilha pelo ID e retorna todos os registros da aba especificada.

    Retorno:
        Lista de dicionários com os dados de cada linha.
    """

    credentials = get_google_credentials()
    gc = gspread.authorize(credentials)

    print(f"Spreadsheet ID: {spreadsheet_id}, Worksheet: {worksheet_name}")

    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(worksheet_name)

    return worksheet.get_all_records(numericise_ignore=["all"])


def format_phone(raw_phone: str) -> str:
    """Remove formatações do número de telefone, deixando apenas dígitos."""

    return (
        str(raw_phone)
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )