# Implantação no Easypanel

Este guia explica como publicar o Monitor.IA no Easypanel usando o Docker Compose deste repositório.

## Como a implantação é organizada

No Easypanel, você cria **um serviço do tipo Compose**. Esse serviço lê `docker/docker-compose.yml` e executa dois containers:

| Serviço | Responsabilidade | Porta interna |
|---|---|---|
| `web` | Nginx serve o frontend e encaminha as requisições da API para o backend. Recebe o tráfego do domínio público. | `80` |
| `backend` | Aplicação Flask executada pelo Gunicorn. Processa as requisições encaminhadas pelo Nginx. | `5001` |

O banco MySQL **não** é criado pelo Compose. Você precisa fornecer um ou mais bancos MySQL acessíveis pelo servidor Easypanel.

## O que você precisa antes de começar

- Um servidor com Easypanel instalado e acesso para criar projetos e serviços.
- Este repositório enviado a um provedor Git que o Easypanel consiga acessar. Para um repositório privado, configure a chave de deploy SSH exibida pelo Easypanel como chave somente de leitura no provedor Git.
- Os dados dos bancos MySQL, usuários e permissões necessários para a aplicação.
- As credenciais e URLs dos serviços externos usados pelo backend.
- Um domínio apontado para o servidor Easypanel, caso queira usar um domínio próprio. O Easypanel também pode fornecer um endereço de serviço.

## 1. Prepare o repositório

Envie ao Git os arquivos de aplicação, incluindo `docker/`, `backend/`, `auth/`, `css/`, `script/` e `assets/`. O build do backend usa o contexto na raiz do repositório.

**Nunca envie o arquivo `.env` com credenciais reais ao Git.** O modelo versionado é `.env.docker.example`; ele pode ser usado como lista das variáveis necessárias. Gere um `JWT_SECRET_KEY` forte e exclusivo para produção. Se uma credencial real já foi compartilhada, substitua-a antes da publicação.

## 2. Crie o serviço Compose no Easypanel

1. No Easypanel, abra um projeto existente ou crie um novo.
2. Selecione **New Service → Compose**.
3. Escolha a origem **Git**.
4. Informe o repositório e a branch que contém o código.
5. Defina:
   - **Build Path:** `/` (raiz do repositório).
   - **Docker Compose File:** `docker/docker-compose.yml`.
6. Salve e abra a seção **Environment** do serviço.

O Compose usa caminhos relativos à raiz do repositório: o Dockerfile está em `docker/Dockerfile`, as configurações do Nginx em `docker/nginx/site.conf` e os arquivos estáticos nas pastas `auth/`, `css/`, `script/` e `assets/`. Portanto, mantenha o Build Path como `/`.

## 3. Configure as variáveis de ambiente

No campo **Environment** do serviço Compose, cadastre as variáveis em formato `NOME=valor`. O Easypanel deve criar o arquivo `.env` na raiz do Build Path (**Create .env file**), pois o Compose carrega esse arquivo em `backend` por meio de `env_file: ../.env`.

Use `.env.docker.example` como referência e preencha os valores reais:

| Categoria | Variáveis | Finalidade |
|---|---|---|
| Banco de login | `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | Configuração da conexão usada pela rota de login. |
| Banco de avaliações e registros | `DB_HOST2`, `DB_PORT2`, `DB_USER2`, `DB_USER22`, `DB_PASSWORD2`, `DB_NAME2` | Configuração das conexões usadas pelas rotas de avaliações, IA e registros. `DB_USER2` e `DB_USER22` são utilizados em rotas distintas e devem ter as permissões necessárias. |
| Autenticação | `JWT_SECRET_KEY`, `JWT_ACCESS_TOKEN_EXPIRES_HOURS` | Define a chave de assinatura e o tempo de validade do token. Utilize um segredo forte e exclusivo em produção. O modelo sugere duração de 4 horas. |
| Gosac | `GOSAC_API_URL`, `GOSAC_API_TOKEN`, `GOSAC_START_PERIOD`, `GOSAC_END_PERIOD` | Configuração da URL, do token e do período da integração com o Gosac. |
| Chatwoot | `CHATWOOT_API_URL`, `CHATWOOT_API_TOKEN` | Configuração da URL e do token de acesso à API do Chatwoot. |
| Google GenAI | `GOOGLE_GENAI_API_KEY` | Chave de acesso aos recursos de inteligência artificial. |
| Planilha | `EXCEL_URL` | URL da planilha utilizada pela integração. |

As variáveis das integrações externas são necessárias para os recursos correspondentes. Se uma integração não estiver configurada, as funções que dependem dela podem falhar mesmo que o site abra.

### Bancos de dados

O Compose não inicializa bancos nem cria tabelas. Antes do deploy, confirme que:

- Os bancos e tabelas requeridos pela aplicação já existem.
- Os usuários têm acesso a partir do IP ou da rede do servidor Easypanel.
- Firewall, regras de rede e lista de IPs permitidos do provedor MySQL aceitam conexões do servidor.
- `DB_USER2` e `DB_USER22` têm as permissões adequadas para as operações que executam.

Se os dois conjuntos de variáveis apontarem para instâncias ou bancos diferentes, ambos precisam estar acessíveis pelo servidor.

## 4. Faça o deploy

1. Confirme que a origem Git, Build Path, caminho do Compose e variáveis estão salvos.
2. Clique em **Deploy**.
3. Aguarde o build da imagem do backend e o início dos containers `backend` e `web`.
4. Abra os logs de cada container se o deploy apresentar erro.

O Dockerfile instala as dependências Python e inicia o Gunicorn na porta `5001`. O Nginx escuta na porta `80` e encaminha as rotas `/webhook/`, `/api/`, `/ia/`, `/avaliacoes/` e `/registro/` para `backend:5001` na rede Compose.

## 5. Configure domínio e HTTPS

1. Abra a seção **Domains** do serviço Compose.
2. Adicione o hostname que deseja usar.
3. Selecione o serviço Compose `web` como destino e informe a porta interna `80` (HTTP).
4. Habilite ou configure o certificado HTTPS no Easypanel.
5. Confirme que o DNS do domínio aponta para o servidor Easypanel.

O domínio deve apontar para `web`, pois é o Nginx que serve o frontend e recebe as requisições do navegador. Não direcione o domínio para `backend:5001` e não é necessário publicar `ports` no host: o proxy do Easypanel encaminha o tráfego ao container `web`.

## 6. Verifique a aplicação

- Abra o domínio. A página inicial do Nginx é `auth/login.html`.
- Verifique o login com uma conta válida.
- Navegue pelas áreas que consultam APIs e integrações.
- Se o site abrir, mas os dados não carregarem, examine os logs do `backend` e valide as conexões de banco e os tokens dos serviços externos.

## Diagnóstico de problemas

| Sintoma | Verificações recomendadas |
|---|---|
| Falha durante o build | Confirme o Build Path `/`, o arquivo `docker/docker-compose.yml`, a existência de `backend/requirements.txt`, `docker/Dockerfile` e dos diretórios referenciados nos volumes. Consulte os logs do Deploy. |
| Container `backend` reinicia | Verifique variáveis ausentes ou inválidas, especialmente `JWT_SECRET_KEY` e as configurações de banco necessárias. Consulte os logs do backend. |
| Erro de conexão MySQL | Confira host, porta, credenciais, nome do banco, permissões (`GRANT`), firewall e lista de IPs autorizados pelo provedor. |
| Domínio não abre | Verifique o DNS, o domínio cadastrado no Easypanel, o destino `web:80` e o estado do container `web`. |
| Página abre, mas a API retorna erro | Consulte os logs do backend, valide as variáveis das integrações e dos bancos e confirme o encaminhamento das rotas pelo Nginx. |
| Alterações no Git não aparecem | Execute um novo Deploy para reconstruir e aplicar as alterações da branch configurada. |

## Atualizações futuras

Envie as alterações para a branch configurada no Easypanel e clique em **Deploy** para reconstruir e aplicar. Após modificar variáveis de ambiente, faça um novo Deploy para que os containers recebam os valores atualizados.

## Execução local com Docker Compose

Para executar em um servidor próprio fora do Easypanel, crie `.env` na raiz a partir de `.env.docker.example`, preencha as variáveis e rode:

```sh
docker compose -f docker/docker-compose.yml up -d --build
```

O Compose não publica uma porta no host; para acesso externo nesse modo, configure seu próprio proxy reverso para encaminhar HTTP à porta `80` do container `web`. No Easypanel, use a configuração de domínio descrita acima.
