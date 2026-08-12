import os

# ── AWS / Secrets Manager ────────────────────────────────────────────────────
SECRET_NAME = os.getenv("SECRET_NAME", "bot-service-sm")
REGION_NAME = os.getenv("REGION_NAME", "sa-east-1")

# ── Google Sheets ────────────────────────────────────────────────────────────
SPREADSHEET_ID_MOTORA = os.getenv(
    "SPREADSHEET_ID_MOTORA", "1Gb1I3lt4p6NQKJX3Og3YjgHBCskX0N_yK06CAxqaAnc"
)
SPREADSHEET_ID_FINAN = os.getenv(
    "SPREADSHEET_ID_FINAN", "1bdZTuGRvy3WYqCn-XW6Ad_ZWXOYl8QT-JgwPzx4RVac"
)

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# ── Dias da semana (pt-BR) ───────────────────────────────────────────────────
DIAS_SEMANA = [
    "segunda",
    "terça",
    "quarta",
    "quinta",
    "sexta",
    "sábado",
    "domingo",
]

# ── Número de alerta do dono da frota ───────────────────────────────────────
OWNER_PHONE = os.getenv("OWNER_PHONE", "5511974654256")
