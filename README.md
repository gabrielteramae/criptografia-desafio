# Criptografia transparente — campos sensíveis cifrados na coluna

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.35-D71F00)
![cryptography](https://img.shields.io/badge/cryptography-43.0.1-555555)

API CRUD de uma entidade com `userDocument` e `creditCardToken`. A cifra não fica no controller: um `TypeDecorator` do SQLAlchemy aplica Fernet na ida e na volta da coluna. `value` permanece inteiro, em claro.

## Por que cifrar na coluna

| Abordagem | O que acontece |
| --- | --- |
| `EncryptedString` na coluna | Rotas, schemas e CRUD trabalham com texto puro. O banco grava o token Fernet. |
| `encrypt()` em cada rota | Qualquer endpoint novo pode esquecer de cifrar ou de decifrar. |
| Cifra no arquivo do banco | Protege o disco, não o valor que um `SELECT` devolve. |

Fernet (pacote `cryptography`) é AES-128-CBC com HMAC. A chave vem de `ENCRYPTION_KEY`. Se a variável não existir, `crypto.py` gera uma chave só para aquele processo: o que foi gravado deixa de abrir no próximo restart. Token inválido na leitura vira `None`, não 500.

A coluna é `String(255)`. O token Fernet é maior que o texto original; documento ou token longos podem não caber.

## Stack

- Python (sem versão pinada no repositório; o código usa sintaxe 3.10+)
- FastAPI 0.115.0 e Uvicorn 0.30.6
- SQLAlchemy 2.0.35
- `cryptography` 43.0.1 (Fernet)
- SQLite por padrão (`sqlite:///./crypto.db`); `DATABASE_URL` troca o dialeto

## Estrutura

```
app/
├── main.py            # CRUD /entities
├── schemas.py         # Pydantic, sempre texto puro
├── crud.py            # persistência, sem chamada a encrypt
├── models.py          # userDocument e creditCardToken como EncryptedString
├── crypto_types.py    # TypeDecorator
├── crypto.py          # Fernet a partir de ENCRYPTION_KEY
└── database.py        # engine e sessão
.env.example
requirements.txt
```

## Como rodar

```bash
git clone https://github.com/gabrielteramae/criptografia-desafio.git
cd criptografia-desafio
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ENCRYPTION_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')"
export DATABASE_URL="${DATABASE_URL:-sqlite:///./crypto.db}"
uvicorn app.main:app --reload
```

Sobe em `http://127.0.0.1:8000`. O OpenAPI gerado pelo FastAPI fica em `/docs`.

## Endpoints

| Método | Rota | Resposta |
| --- | --- | --- |
| GET | `/` | `{"status":"ok","service":"crypto-transparent-api"}` |
| POST | `/entities` | 201, corpo com `userDocument`, `creditCardToken`, `value` |
| GET | `/entities` | lista; query `skip` (padrão 0) e `limit` (padrão 100) |
| GET | `/entities/{entity_id}` | 404 se não existir |
| PUT | `/entities/{entity_id}` | substitui os três campos |
| DELETE | `/entities/{entity_id}` | 204 |

## O que não tem

Não há testes automatizados. Não há rotação de chave, nem cifra de `value`, nem Docker.

---

© 2026 Gabriel Teramae Chan
