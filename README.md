# Crypto Transparent API

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/AES-Fernet-black?logo=letsencrypt&logoColor=white)

Solução para o desafio [`backend-br/desafios/cryptography`](https://github.com/backend-br/desafios/blob/master/cryptography/PROBLEM.md): implementar criptografia transparente em campos sensíveis de uma entidade, sem que a camada de API ou a lógica de negócio precise conhecer o processo de cifrar/decifrar.

## Ideia da solução

Os campos `userDocument` e `creditCardToken` nunca trafegam em texto puro para o banco. A conversão acontece automaticamente na camada de persistência através de um `TypeDecorator` do SQLAlchemy, então o resto da aplicação (rotas, schemas, regras de negócio) trabalha sempre com os valores originais.

```
Request  -> Pydantic (texto puro) -> SQLAlchemy model -> EncryptedString.process_bind_param()  -> AES  -> banco
Response <- Pydantic (texto puro) <- SQLAlchemy model <- EncryptedString.process_result_value() <- AES  <- banco
```

Isso garante que:
- Ninguém com acesso direto ao banco enxerga os dados sensíveis.
- Nenhuma rota, service ou schema precisa chamar `encrypt`/`decrypt` manualmente.
- Trocar o algoritmo de criptografia no futuro exige mudar apenas `crypto.py`.

## Stack

- **FastAPI** para a API REST
- **SQLAlchemy 2.0** com um `TypeDecorator` customizado (`EncryptedString`)
- **cryptography.Fernet** (AES-128-CBC + HMAC autenticado) para a cifragem simétrica
- **SQLite** por padrão (`DATABASE_URL` configurável para Postgres/MySQL)

## Estrutura

```
app/
├── main.py          # rotas da API (CRUD)
├── models.py         # entidade SQLAlchemy
├── schemas.py         # schemas Pydantic (sempre texto puro)
├── crud.py            # operações de banco
├── crypto.py           # encrypt/decrypt com Fernet
└── crypto_types.py      # TypeDecorator que aplica a criptografia nas colunas
```

## Como rodar

```bash
git clone https://github.com/gabrielteramae/criptografia-desafio.git
cd criptografia-desafio
pip install -r requirements.txt

export ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. Docs interativas em `/docs`.

> Se `ENCRYPTION_KEY` não for definida, uma chave temporária é gerada em runtime (útil só para teste local — em produção sempre defina a variável de ambiente, senão os dados gravados se tornam ilegíveis a cada restart).

## Endpoints

| Método | Rota               | Descrição            |
|--------|---------------------|------------------------|
| POST   | `/entities`          | Cria uma entidade      |
| GET    | `/entities`           | Lista entidades         |
| GET    | `/entities/{id}`       | Busca por id             |
| PUT    | `/entities/{id}`        | Atualiza por id            |
| DELETE | `/entities/{id}`         | Remove por id                |

## Exemplo

```bash
curl -X POST http://localhost:8000/entities \
  -H "Content-Type: application/json" \
  -d '{"userDocument":"123.456.789-00","creditCardToken":"tok_abc123","value":5999}'
```

Resposta da API (texto puro):

```json
{"id": 1, "userDocument": "123.456.789-00", "creditCardToken": "tok_abc123", "value": 5999}
```

O que fica gravado no banco (criptografado):

```
id | userDocument                                    | creditCardToken                                 | value
1  | gAAAAABqWAeipNX_xTJV7gaLYqz7Rl27k5B9EJ5oKoEn...  | gAAAAABqWAeiSu-WIpoEBuUnmAl9hEThoEeBGYMzNF-Y...  | 5999
```

---

© 2026 Gabriel Teramae Chan
