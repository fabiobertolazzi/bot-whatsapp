def mensagem_checklist_segunda() -> str:
    """Mensagem de checklist semanal enviada às segundas-feiras."""
    return (
        "☀️ Bom dia!!!\n\n"
        "📌 Lembrete importante:\n\n"
        "Segunda-feira é dia perfeito pra dar esse check rápido no carro antes da correria da semana 👀 :\n\n"
        "Checklist de 2 minutos:\n\n"
        "  🛠️ ⁠Óleo do motor: Vareta no nível, com motor frio e carro plano;\n"
        "⁠  💧 ⁠Água do radiador: Reservatório entre mín e máx. ⚠️ Só abra com motor frio!\n"
        "⁠  🛞 ⁠Pneus: Calibre com eles frios. No Mobi Like é 32-35 PSI, mas confira a etiqueta da porta;\n"
        "⁠  🚘 ⁠Extra: Dê uma olhada se não tem poça embaixo do carro;\n\n"
        "✅ Cuidar disso na segunda evita dor de cabeça no resto da semana. Tenha um ótimo trabalho!!!\n\n"
    )


def mensagem_cobranca(nome: str) -> str:
    """Mensagem de lembrete de pagamento enviada no dia do vencimento."""
    return (
        f"🚗 Olá *{nome}*, bom dia!!!\n\n"
        "📅 Lembrete:\n\n"
        "💰 O aluguel vence hoje! Por favor, efetue o pagamento até o final do dia "
        "para evitar o BLOQUEIO do seu veículo.\n\n"
        "Se você já realizou o pagamento, por favor, desconsidere esta mensagem.\n\n"
        "Favor enviar também um vídeo rápido do veículo, mostrando quilometragem e as "
        "condições gerais do carro, inclusive com o adesivo com a última troca de óleo.\n\n"
        "Obrigado e tenha uma ótima semana! 🙌"
    )

def mensagem_vencimento_dia(data: str, id: str, categoria: str, situacao: str, valor: str) -> str:
    """Mensagem de informações financeiras enviada no dia."""
    return (
        "☀️ Bom dia empreendedores ☀️\n"
        "📅 Hoje temos pagamentos a realizar:\n\n"
        f"Data: {data}\n"
        f"ID: {id}\n"
        f"Categoria: {categoria}\n"
        f"Situação: {situacao}\n"
        f"Valor: {valor}\n"
        "📌 Ao pagar o boleto, dar baixa na planilha e enviar o comprovante para o grupo de WhatsApp da frota.\n\n"
    )


def mensagem_saldo(data: str, valor: str) -> str:
    """Mensagem de saldo do dia."""
    return (
        "☀️ Bom dia empreendedores ☀️\n"
        f"💰 O saldo da nossa empresa em {data} é de {valor}.\n"
        "Vamos em frente!!!\n\n"
    )

def mensagem_bot_ativo() -> str:
    """Mensagem de heartbeat enviada quando não há ação para o dia."""
    return (
        "Essa mensagem é só para garantir que o bot tá funcionando, "
        "mas hoje não tem nenhum pagamento vencendo e nem é segunda-feira, "
        "então relaxa e aproveita o dia!!!"
    )
