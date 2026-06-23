import pandas as pd
from datetime import datetime
from supabase import create_client, Client
from banco_dados import cardapio

# 🌐 CREDENCIAIS HTTP DO SUPABASE
SUPABASE_URL = "https://cljhklrjrcgtwdudfesg.supabase.co"
SUPABASE_KEY = "sb_publishable_bnU7EK6EBN6UvaKNJmu-1g_pD6VSqcv"

# Inicializa o cliente web seguro
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def registrar_venda_banco(carrinho):
    """Grava os itens via requisição HTTPS na tabela do banco."""
    if not carrinho:
        return False
        
    novos_registros = []
    data_hora_atual = datetime.now().isoformat() # Formato de texto aceito via API
    
    for item in carrinho:
        # Recupera o preço unitário do item
        preco_unit = float(cardapio.get(item["produto"], 0.0))
        
        novos_registros.append({
            "data_hora": data_hora_atual,
            "produto": item["produto"],
            "quantidade": int(item["quantidade"]),
            "preco_unitario": preco_unit,
            "total": float(item["total"])
        })
    
    # Envia os dados usando protocolo de internet comum (Porta 443)
    supabase.table("vendas").insert(novos_registros).execute()
    return True

def obter_dataframe_vendas():
    """Busca o histórico via requisição HTTPS."""
    resposta = supabase.table("vendas").select("*").execute()
    df = pd.DataFrame(resposta.data)
    
    if not df.empty:
        df["data_hora"] = pd.to_datetime(df["data_hora"])
        df = df.sort_values(by="data_hora", ascending=False)
        df = df.head(10)
    return df

def calcular_faturamento_periodo():
    """Busca os dados via HTTPS e calcula os faturamentos usando Pandas."""
    resposta = supabase.table("vendas").select("*").execute()
    df = pd.DataFrame(resposta.data)
    
    if df.empty:
        return 0.0, 0.0
        
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    agora = datetime.now()
    
    filtro_dia = (
        (df["data_hora"].dt.year == agora.year) &
        (df["data_hora"].dt.month == agora.month) &
        (df["data_hora"].dt.day == agora.day)
    )
    
    filtro_mes = (
        (df["data_hora"].dt.year == agora.year) &
        (df["data_hora"].dt.month == agora.month)
    )
    
    faturamento_diario = float(df[filtro_dia]["total"].sum())
    faturamento_mensal = float(df[filtro_mes]["total"].sum())
    
    return faturamento_diario, faturamento_mensal

def calcular_total_item(item, quantidade):
    """
    Calcula o valor total de um item.
    Funciona recebendo tanto o nome em formato string quanto o dicionário do cardápio.
    """
    if isinstance(item, dict):
        preco_unitario = float(item.get("preco", 0.0))
    else:
        # Se vier apenas a string (ex: 'Coxinha'), busca o preço no dicionário do cardápio
        preco_unitario = float(cardapio.get(item, 0.0))
        
    return float(preco_unitario * quantidade)