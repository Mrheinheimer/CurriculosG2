# Sistema de Cadastro de Currículos - Flask

Projeto desenvolvido para o trabalho de G2: sistema WEB para cadastro, listagem e consulta de currículos.

## Funcionalidades

- Tela 1: listagem dos currículos cadastrados, exibindo nome e e-mail.
- Tela 2: cadastro de novo currículo.
- Tela 3: consulta completa do currículo selecionado.

## Campos

- Nome da pessoa: obrigatório.
- Telefone: opcional.
- E-mail: obrigatório.
- Endereço WEB: opcional.
- Experiência profissional: obrigatório.

## Segurança implementada

- Proteção contra SQL Injection usando consultas parametrizadas com `?` no SQLite.
- Proteção contra XSS usando escape automático do Jinja2 e não usando `|safe` nos dados do usuário.
- Content Security Policy bloqueando scripts externos e inline.
- Proteção contra clickjacking/history manipulation com `X-Frame-Options: DENY` e `frame-ancestors 'none'`.
- Cache desabilitado com `Cache-Control: no-store` para evitar exibição indevida de páginas antigas pelo histórico.
