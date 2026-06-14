# Projeto de Indicador

Aplicação Flask simples que consulta um banco de dados SQL Server e gera relatórios em Excel.

## Requisitos

- Python 3.10+ (recomendado)
- ODBC Driver 17 for SQL Server instalado
- Conexão com banco SQL Server

## Dependências

Instale as dependências usando:

```bash
pip install -r requirements.txt
```

## Configuração

Copie o arquivo `.env` e preencha os valores do banco de dados:

```env
DB_DRIVER="ODBC Driver 17 for SQL Server"
DB_SERVER="SEU_SERVIDOR"
DB_DATABASE="SEU_BANCO"
DB_TRUSTED_CONNECTION="yes"
```

> Se você usar autenticação SQL, atualize a string de conexão no código ou adicione variáveis adicionais.

## Executando

```bash
python indicador.py
```

Acesse a aplicação em `http://127.0.0.1:5000/`.

## Rotas

- `/` — página inicial com valores de clientes, pedidos e produtos
- `/download/clientes` — baixa planilha de clientes
- `/download/pedidos` — baixa planilha de pedidos
- `/download/produtos` — baixa planilha de produtos

## Estrutura do projeto

- `indicador.py` — aplicação Flask
- `.env` — configuração do banco de dados
- `templates/index.html` — template da página principal
