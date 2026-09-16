# Backend de avaliações

API Flask que fornece as avaliações da tabela `avaliacao_atendimentos`.

## 1. Ambiente virtual (Windows)

No PowerShell, dentro de `backend`:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se necessário: `Set-ExecutionPolicy -Scope Process Bypass`.

## 2. Dependências

```powershell
pip install -r requirements.txt
```

## 3. Arquivo `.env`

```powershell
Copy-Item .env.example .env
```

Preencha `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`,
`MYSQL_DATABASE` e `JWT_SECRET_KEY`. Nunca versione este arquivo.

## 4. MySQL e execução

A tabela `avaliacao_atendimentos` deve conter os campos consultados em
`routes/avaliacoes.py`. Inicie o servidor:

```powershell
python app.py
```

Ele ficará em `http://127.0.0.1:5001` por padrão. Para usar outra porta,
defina `AVALIACOES_PORT` antes de iniciá-lo.

## 5. Testar

Consulte a rota informando o período desejado:

```powershell
Invoke-RestMethod "http://127.0.0.1:5001/api/avaliacoes?data_inicial=2026-09-01&data_final=2026-09-10"
```

Resposta:

```json
{"registros":[{"id":1,"identificador_unico":"ABC123","data":"2026-09-10T14:30:00","canal":"WhatsApp","beneficiario":"João","score_qualidade":9.2,"risco_processo":"Baixo","resolvido":"Sim","conversacao":{},"criado_em":"2026-09-10T14:35:00"}]}
```

Sem resultados, a API responde `200` com `{"registros": []}`. Parâmetros
inválidos retornam `400`, e JWT ausente, inválido ou expirado retorna `401`.
Erros técnicos são registrados no backend sem expor credenciais ao frontend.
