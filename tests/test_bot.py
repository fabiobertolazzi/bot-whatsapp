"""
Testes unitários — rode com:  pytest tests/ -v
"""

import pytest
from unittest.mock import MagicMock, patch

# ─────────────────────────────────────────────────────────────────────────────
# messages.py
# ─────────────────────────────────────────────────────────────────────────────

from src.messages import (
    mensagem_bot_ativo,
    mensagem_checklist_segunda,
    mensagem_cobranca,
)


class TestMessages:
    def test_checklist_segunda_contem_oleos(self):
        msg = mensagem_checklist_segunda()
        assert "Óleo do motor" in msg

    def test_cobranca_contem_nome(self):
        msg = mensagem_cobranca("João")
        assert "João" in msg

    def test_cobranca_menciona_bloqueio(self):
        msg = mensagem_cobranca("Maria")
        assert "BLOQUEIO" in msg

    def test_bot_ativo_e_string(self):
        msg = mensagem_bot_ativo()
        assert isinstance(msg, str)
        assert len(msg) > 0


# ─────────────────────────────────────────────────────────────────────────────
# sheets.py
# ─────────────────────────────────────────────────────────────────────────────

from src.sheets import format_phone


class TestFormatPhone:
    def test_remove_espacos(self):
        assert format_phone("55 11 99999-9999") == "5511999999999"

    def test_remove_parenteses(self):
        assert format_phone("(11) 99999-9999") == "1199999999"

    def test_numero_limpo_inalterado(self):
        assert format_phone("5511999999999") == "5511999999999"


# ─────────────────────────────────────────────────────────────────────────────
# whatsapp.py
# ─────────────────────────────────────────────────────────────────────────────

class TestSendWhatsapp:

    @patch("src.whatsapp.get_meta_token", return_value="fake-token")
    @patch("src.whatsapp.get_phone_number_id", return_value="123456")
    @patch("src.whatsapp.requests.post")
    def test_envia_com_sucesso(self, mock_post, mock_pid, mock_token):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"messages":[{"id":"wamid.xxx"}]}'
        mock_post.return_value = mock_response

        from src.whatsapp import send_whatsapp
        result = send_whatsapp("5511999999999", "Olá!")

        assert result["status_code"] == 200
        mock_post.assert_called_once()

    @patch("src.whatsapp.get_meta_token", return_value="fake-token")
    @patch("src.whatsapp.get_phone_number_id", return_value="123456")
    @patch("src.whatsapp.requests.post")
    def test_levanta_excecao_em_erro(self, mock_post, mock_pid, mock_token):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        from src.whatsapp import send_whatsapp
        with pytest.raises(Exception, match="Erro WhatsApp API"):
            send_whatsapp("5511999999999", "Olá!")


# ─────────────────────────────────────────────────────────────────────────────
# handler.py (integração simulada)
# ─────────────────────────────────────────────────────────────────────────────

class TestLambdaHandler:

    @patch("src.handler.datetime")
    @patch("src.handler.get_sheet_records")
    @patch("src.handler.send_whatsapp")
    def test_segunda_envia_checklist(
        self, mock_send, mock_records, mock_dt
    ):
        # Simula uma segunda-feira
        mock_dt.now.return_value.weekday.return_value = 0
        mock_records.return_value = []

        from src.handler import lambda_handler
        result = lambda_handler({}, {})

        assert result["statusCode"] == 200
        # O primeiro envio deve ser o checklist
        primeiro_envio = mock_send.call_args_list[0]
        assert "Óleo do motor" in primeiro_envio[0][1]

    @patch("src.handler.datetime")
    @patch("src.handler.get_sheet_records")
    @patch("src.handler.send_whatsapp")
    def test_sem_pagamentos_envia_heartbeat(
        self, mock_send, mock_records, mock_dt
    ):
        # Simula uma quarta-feira sem vencimentos
        mock_dt.now.return_value.weekday.return_value = 2
        mock_records.return_value = []

        from src.handler import lambda_handler
        lambda_handler({}, {})

        # Deve enviar apenas o heartbeat
        assert mock_send.call_count == 1
        heartbeat_msg = mock_send.call_args[0][1]
        assert "bot tá funcionando" in heartbeat_msg

    @patch("src.handler.datetime")
    @patch("src.handler.get_sheet_records")
    @patch("src.handler.send_whatsapp")
    def test_motorista_ativo_recebe_cobranca(
        self, mock_send, mock_records, mock_dt
    ):
        # Simula uma terça com 1 motorista ativo
        mock_dt.now.return_value.weekday.return_value = 1
        mock_records.return_value = [
            {
                "Nome": "Carlos",
                "Status": "Ativo",
                "Telefone": "5511988887777",
                "Dia da Semana": "terça",
            }
        ]

        from src.handler import lambda_handler
        lambda_handler({}, {})

        numeros_chamados = [c[0][0] for c in mock_send.call_args_list]
        assert "5511988887777" in numeros_chamados
