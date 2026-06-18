import os
from datetime import datetime
import pandas as pd
from banco_dados import cardapio

ARQUIVO_VENDAS = "vendas.csv"

def inicializar_arquivo_vendas():
    if not os.path.exists(ARQUIVO_VENDAS):
        df_vazio = pd.DataFrame(columns=["data_hora", "produto", "quantidade", "total"])
        df_vazio.to_csv(ARQUIVO_VENDAS, index=False)

def calcular_total_item(produto, quantidade):
    return cardapio[produto] * quantidade

def registrar_carrinho_no_banco(carrinho):
    if not carrinho:
        return
        
    inicializar_arquivo_vendas()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    novas_linhas = []
    for item in carrinho:
        novas_linhas.append({
            "data_hora": agora,
            "produto": item["produto"],
            "quantidade": item["quantidade"],
            "total": item["total"]
        })
        
    df_existente = pd.read_csv(ARQUIVO_VENDAS)
    df_novas_vendas = pd.DataFrame(novas_linhas)
    
    df_atualizado = pd.concat([df_existente, df_novas_vendas], ignore_index=True)
    df_atualizado.to_csv(ARQUIVO_VENDAS, index=False)

def obter_dataframe_vendas():
    """Retorna o DataFrame completo, mas ordenado com as vendas mais recentes primeiro."""
    inicializar_arquivo_vendas()
    df = pd.read_csv(ARQUIVO_VENDAS)
    
    if not df.empty:
        # Ordena pela coluna data_hora de forma decrescente (ascending=False)
        df = df.sort_values(by="data_hora", ascending=False)
        df = df.head(20)
        
    return df

def calcular_faturamento_periodo():
    """Calcula o faturamento do dia de hoje e do mês atual usando filtros do Pandas."""
    inicializar_arquivo_vendas()
    df = pd.read_csv(ARQUIVO_VENDAS)
    
    if df.empty:
        return 0.0, 0.0
        
    # Garante que o Pandas entende a coluna como data/hora, exatamente como no seu exercício!
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    
    hoje = datetime.now().date()
    mes_atual = datetime.now().month
    ano_current = datetime.now().year
    
    # Filtro booleano para hoje
    df_hoje = df[df["data_hora"].dt.date == hoje]
    faturamento_diario = df_hoje["total"].sum()
    
    # Filtro booleano para o mês e ano atuais
    df_mes = df[(df["data_hora"].dt.month == mes_atual) & (df["data_hora"].dt.year == ano_current)]
    faturamento_mensal = df_mes["total"].sum()
    
    return faturamento_diario, faturamento_mensal