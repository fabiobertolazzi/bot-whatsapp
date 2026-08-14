import json
from datetime import datetime

from src.config import DIAS_SEMANA, OWNER_PHONE
from src.messages import (
    mensagem_bot_ativo,
    mensagem_checklist_segunda,
    mensagem_cobranca,
    mensagem_vencimento_dia,
    mensagem_saldo
)
from src.sheets import format_phone, get_sheet_records, SPREADSHEET_ID_MOTORA, SPREADSHEET_ID_FINAN
from src.whatsapp import send_whatsapp


def lambda_handler(event, context):
    """
    Ponto de entrada da Lambda.

    Fluxo:
      1. Descobre o dia da semana atual.
      2. Se for segunda, envia checklist de manutenção ao dono da frota.
      3. Para cada motorista ativo com vencimento hoje, envia cobrança.
      4. Se não houve nenhum envio, manda heartbeat ao dono da frota.
      --Fluxo financeiro (em desenvolvimento)--
    """
    hoje = DIAS_SEMANA[datetime.now().weekday()]
    print(f"[Handler] Dia atual: {hoje}")

    enviou_algo = False

    # ── 1. Checklist de segunda-feira ────────────────────────────────────────
    if hoje == "segunda":
        send_whatsapp(OWNER_PHONE, mensagem_checklist_segunda())
        enviou_algo = True

    # ── 2. Cobranças do dia ──────────────────────────────────────────────────
    data_motora = get_sheet_records(SPREADSHEET_ID_MOTORA,"Sheet1")
    results = []

    for row in data_motora:
        dia_pagamento = row.get("Dia da Semana", "").strip().lower()

        if dia_pagamento != hoje:
            continue

        nome = row.get("Nome")
        status = row.get("Status")
        phone = format_phone(row.get("Telefone", ""))
        mensagem = mensagem_cobranca(nome)

        if status == "Ativo":
            send_whatsapp(phone, mensagem)
            enviou_algo = True

        results.append({"phone": phone, "nome": nome, "status": status})

    # ── 3. Heartbeat (nenhum envio no dia) ───────────────────────────────────
    #if not enviou_algo:
    #    send_whatsapp(OWNER_PHONE, mensagem_bot_ativo())



    # ── 4. Financeiro do dia ──────────────────────────────────────────────────
    data_finan = get_sheet_records(SPREADSHEET_ID_FINAN,"Sheet1")
    results = []

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    for row in data_finan:
        data = row.get("Data")
        if data == data_hoje and row.get("Categoria") != "Aluguel":
            data = row.get("Data")
            id = row.get("ID")
            categoria = row.get("Categoria")
            situacao = row.get("Situação")
            valor = row.get("Valor")

            mensagem = mensagem_vencimento_dia(data, id, categoria, situacao, valor)
            send_whatsapp(OWNER_PHONE, mensagem)
        
        results.append({"Data": data})

    # ── 5. Saldo do dia ──────────────────────────────────────────────────
    saldo_dia = get_sheet_records(SPREADSHEET_ID_FINAN,"Saldo")
    results = []

    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    for row in saldo_dia:
        valor = format(row.get("Valor"), ".2f")

        mensagem = mensagem_saldo(data_hoje, valor)
        send_whatsapp(OWNER_PHONE, mensagem)
        
        results.append({"Data": data})


    return {
        "statusCode": 200,
        "body": json.dumps({"dia": hoje, "processados": results}),
    }
