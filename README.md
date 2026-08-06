# 🚗 Bot WhatsApp — Frota de Veículos

Bot serverless (AWS Lambda) que envia lembretes automáticos via WhatsApp para motoristas de aplicativo, incluindo cobranças de aluguel e checklist semanal de manutenção.

---

## 📁 Estrutura do projeto

```
bot-whatsapp/
├── src/
│   ├── config.py       # Constantes e variáveis de ambiente
│   ├── secrets.py      # Integração com AWS Secrets Manager
│   ├── sheets.py       # Leitura da planilha Google Sheets
│   ├── whatsapp.py     # Envio de mensagens via Meta API
│   ├── messages.py     # Textos das mensagens do bot
│   └── handler.py      # Lambda handler (lógica principal)
├── tests/
│   └── test_bot.py     # Testes unitários
├── scripts/
│   └── run_local.py    # Execução local do bot
├── .env.example        # Modelo de variáveis de ambiente
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Como rodar localmente

### 1. Clonar o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd bot-whatsapp
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com seus valores reais
```

### 5. Executar o bot localmente

```bash
python scripts/run_local.py
```

---

## 🧪 Rodar os testes

```bash
pytest tests/ -v
```

---

## ☁️ Deploy na AWS Lambda

O arquivo de entrada da Lambda deve ser `src/handler.py` e a função handler é `lambda_handler`.

Empacote e faça o deploy normalmente via console ou AWS CLI:

```bash
zip -r function.zip src/ requirements.txt
aws lambda update-function-code \
  --function-name nome-da-sua-lambda \
  --zip-file fileb://function.zip
```

---

## 🔗 Sincronização GitHub ↔ AWS CodeCommit

### Configurar dois remotos

```bash
# Remoto principal (GitHub)
git remote add origin https://github.com/fabiobertolazzi/bot-whatsapp.git

# Remoto secundário (CodeCommit)
git remote add codecommit https://git-codecommit.sa-east-1.amazonaws.com/v1/repos/bot-whatsapp
```

### Push para os dois ao mesmo tempo

```bash
# Empurra para ambos de uma vez
git push origin main
git push codecommit main
```

### Ou configure o push automático para múltiplos remotos

```bash
git remote set-url --add --push origin https://github.com/seu-usuario/bot-whatsapp.git
git remote set-url --add --push origin https://git-codecommit.sa-east-1.amazonaws.com/v1/repos/bot-whatsapp

# Agora um único "git push" envia para os dois
git push
```

---

## 🔐 Secrets no AWS Secrets Manager

O segredo `bot-service-sm` deve conter as seguintes chaves:

| Chave | Descrição |
|---|---|
| `meta_token` | Token da Meta / WhatsApp Business API |
| `phone_number_id` | ID do número de telefone na Meta |
| `type` | `service_account` (Google) |
| `project_id` | ID do projeto no Google Cloud |
| `private_key_id` | ID da chave privada |
| `private_key` | Chave privada RSA |
| `client_email` | E-mail da service account |
| `client_id` | ID do cliente |
| `auth_uri` | URI de autenticação Google |
| `token_uri` | URI de token Google |
| `auth_provider_x509_cert_url` | URL do certificado |
| `client_x509_cert_url` | URL do certificado do cliente |
