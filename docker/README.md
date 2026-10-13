# Deploy

No servidor Linux com Docker Compose instalado:

1. Copie `.env.docker.example` para `.env` na raiz do projeto e preencha os bancos e as chaves dos serviços externos. `DB_USER2` e `DB_USER22` são usados em rotas diferentes e precisam apontar para o usuário correto do banco de avaliações.
2. Inicie a aplicação na raiz do projeto:

   ```sh
   docker compose -f docker/docker-compose.yml up -d --build
   ```

3. Acesse `http://<IP-ou-domínio-do-servidor>/`. Para usar outra porta, defina `WEB_PORT` no `.env`.

O Nginx serve o frontend e encaminha as rotas da API ao backend. O banco é externo e configurado pelas variáveis do `.env`; não há banco local criado pelo Compose.

Antes de colocar no ar, gere novas credenciais para qualquer segredo que já tenha sido compartilhado e use os novos valores no `.env` do servidor. Não envie esse arquivo ao repositório.
