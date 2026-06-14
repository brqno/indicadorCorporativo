from flask import Flask, render_template, send_file
import pyodbc
import pandas as pd
import io
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def conectar():
    DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    SERVER = os.getenv('DB_SERVER')
    DATABASE = os.getenv('DB_DATABASE')
    TRUSTED_CONNECTION = os.getenv('DB_TRUSTED_CONNECTION', 'yes')

    if not SERVER or not DATABASE:
        raise ValueError('As variáveis de ambiente DB_SERVER e DB_DATABASE devem estar definidas.')

    return pyodbc.connect(
        f'DRIVER={{{DRIVER}}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'Trusted_Connection={TRUSTED_CONNECTION};',
        timeout=10
    )

def consultar_clientes():
    conn = conectar()
    df = pd.read_sql("SELECT COUNT(ClienteId) AS Total FROM TB_CLIENTE", conn)
    conn.close()
    return int(df['Total'].iloc[0])

def consultar_pedidos():
    conn = conectar()
    df = pd.read_sql("SELECT COUNT(NumeroPedido) AS Total FROM TB_PEDIDO", conn)
    conn.close()
    return int(df['Total'].iloc[0])

def consultar_produtos():
    conn = conectar()
    df = pd.read_sql("SELECT COUNT(ProdutoId) AS Total FROM TB_PRODUTO", conn)
    conn.close()
    return int(df['Total'].iloc[0])

def gerar_excel(query, nome_arquivo):
    try:
        conn = conectar()
        df = pd.read_sql(query, conn)
        conn.close()
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados')
        
        output.seek(0)
        
        return send_file(
            output, 
            as_attachment=True, 
            download_name=f"{nome_arquivo}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return f"Erro ao gerar arquivo: {str(e)}"

@app.route("/download/clientes")
def download_clientes():
    return gerar_excel("SELECT * FROM TB_CLIENTE", "Relatorio_Clientes")

@app.route("/download/pedidos")
def download_pedidos():
    return gerar_excel("SELECT * FROM TB_PEDIDO", "Relatorio_Pedidos")

@app.route("/download/produtos")
def download_produtos():
    return gerar_excel("SELECT * FROM TB_PRODUTO", "Relatorio_Produtos")

@app.route("/")
def home():
    dados = {
        "valor_clientes": consultar_clientes(),
        "valor_pedidos": consultar_pedidos(),
        "valor_produtos": consultar_produtos()
    }
    return render_template("index.html", **dados)

if __name__ == "__main__":
    app.run(debug=True)