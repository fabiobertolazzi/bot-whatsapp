"""
Execução local do bot.

Como usar:
  1. Copie o arquivo .env.example para .env e preencha os valores.
  2. Execute:  python scripts/run_local.py
"""

import os
import sys

# Garante que o diretório raiz do projeto está no path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

# Ativa o modo local (usa variáveis de ambiente em vez da AWS)
os.environ.setdefault("LOCAL_MODE", "true")

from src.handler import lambda_handler

if __name__ == "__main__":
    print("=" * 50)
    print("  Bot WhatsApp — Execução Local")
    print("=" * 50)

    result = lambda_handler(event={}, context={})

    print("\n[Resultado]")
    print(result)
