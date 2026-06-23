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

## Como rodar no computador

1. Instale o Python 3.
2. Abra o terminal dentro da pasta do projeto.
3. Crie o ambiente virtual:

```bash
python -m venv venv
```

4. Ative o ambiente virtual:

No Windows:

```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

5. Instale as dependências:

```bash
pip install -r requirements.txt
```

6. Rode o sistema:

```bash
python app.py
```

7. Abra no navegador:

```text
http://127.0.0.1:5000
```

## Como publicar na nuvem usando Render

1. Crie uma conta no GitHub.
2. Crie um repositório público.
3. Envie todos os arquivos deste projeto para o repositório.
4. Crie uma conta no Render.
5. Clique em New + > Web Service.
6. Conecte o repositório do GitHub.
7. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
8. Clique em Deploy.
9. O Render vai gerar um link público para acessar o sistema em outra máquina.

## Observação sobre SQLite na nuvem

Este projeto usa SQLite para simplificar o trabalho. Em alguns serviços gratuitos, os dados podem ser apagados quando o servidor reinicia. Para apresentação do trabalho, normalmente isso é suficiente. Para uso real, o ideal é usar PostgreSQL.
