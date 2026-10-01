# Loja Architech

## Como rodar

1. Criar e ativar o ambiente virtual:

```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
```

   No Linux/Mac: `source .venv/bin/activate`

2. Instalar as dependências:

```
   pip install -r requirements.txt
```

3. Criar o arquivo de segredos a partir do modelo:

```powershell
   copy .secrets.toml.example .secrets.toml
```

   No Linux/Mac: `cp .secrets.toml.example .secrets.toml`

4. Rodar:

```
   flask run
```

## Acesso administrativo

- Painel: http://127.0.0.1:5000/admin/
- Usuário: `admin`
- Senha: `BridgeLab` (definida no `.secrets.toml`)
- Para sair: menu do usuário na loja (`/main/v1/`) > Sair

## Segurança

- Senhas armazenadas com hash scrypt + salt (nunca em texto puro).
- Segredos fora do código; o `.secrets.toml` real está no `.gitignore`.
- Em produção, usar as variáveis de ambiente `FLASK_SECRET_KEY` e `FLASK_ADMIN_PASSWORD`.