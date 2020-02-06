# Credentials

--- 
## Configurações dos arquivos
    Configure todos arquivo dentro desta pasta
#### client_secret.json
> Para conseguir a comunicação com o Google Drive é necessário 
> habilitar a API no Google Cloud 

- Entre no [Google API Console](https://console.developers.google.com/)
- No topo da página, próximo ao logo da Google API, selecione seu projeto. O painel de serviços vai aparecer.
- No botão de API's e Serviços, clique em **Google Drive API**, Se você não ve esta opção você deve [habilitar Google Drive API](https://developers.google.com/drive/api/v3/enable-drive-api).
- Volte para Dashboard de API's e Serviços, e clique em **Google Sheets API**.
- No barra de navegação a esquerda, clique em **Credentials**.
- Siga os passos para criar a credencial e faça o download do arquivo `.json`.

#### credentials.txt
> Configurações para acessar o banco de dados, limitado ao MySQL e MariaDB.

**Variaveis**:
- **user** - Usuário de acesso a base
- **password** - Senha referente ao usuário de acesso
- **host** - Endereço IP em que se encontra a base
- **port** - Porta de acesso
- **db** - Nome da base de dados (schema)   

Substitua no exemplo abaixo:

`user:password@host:port/db`
