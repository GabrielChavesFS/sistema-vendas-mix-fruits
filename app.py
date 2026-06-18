import streamlit as st
import operacoes
from banco_dados import cardapio

st.set_page_config(page_title="Caixa Mix Fruits", page_icon="🍇", layout="wide")

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

st.title("🍇 Sistema de Vendas - Mix Fruits")

aba_caixa, aba_historico = st.tabs(["🛍️ Tela de Vendas", "📊 Painel Gerencial"])

with aba_caixa:
    col_cardapio, col_pedido = st.columns([1.5, 1], gap="large")
    
    with col_cardapio:
        st.subheader("📋 Cardápio")
        
        cat_salgados = ["Coxinha", "Coxinha c/ Catupiry", "Quibe", "Enrolado de Presunto", "Enrolado de Salsicha", "Pastel Assado", "Esfirra", "Empada", "Hamburgão", "Mini Pizza", "Pão de Queijo", "Pão de Queijo c/ Linguiça", "Pão com Manteiga", "Misto Quente", "Pão com Ovo"]
        cat_sucos_acai = ["Suco Natural 300ML", "Suco Natural 500ML", "Suco Natural 700ML", "Creme de Açaí 300ML", "Creme de Açaí 500ML", "Creme de Açaí 700ML", "Vitamina de Açaí 300ML", "Vitamina de Açaí 500ML", "Vitamina de Açaí 700ML"]
        cat_bebidas_cafes = ["Refrigerante 200ml", "Energético Monster", "Gatorade", "Água c/ gás", "Água s/ gás", "Kaiser", "Brahma", "Original", "Spaten", "Stella Artois", "Heineken", "Café", "Café com leite", "Achocolatado", "Capuccino"]
        
        def renderizar_categoria(lista_itens, chave_cat):
            for item in lista_itens:
                if item in cardapio:
                    c1, c2, c3 = st.columns([3, 1.5, 2])
                    with c1:
                        st.markdown(f"**{item}**\n\n*R$ {cardapio[item]:.2f}*")
                    with c2:
                        qtd = st.number_input("Qtd:", min_value=1, value=1, step=1, key=f"qtd_{chave_cat}_{item}")
                    with c3:
                        st.write("")
                        st.write("") 
                        if st.button("➕ Adicionar", key=f"add_{chave_cat}_{item}", use_container_width=True):
                            total_item = operacoes.calcular_total_item(item, qtd)
                            st.session_state.carrinho.append({
                                "produto": item,
                                "quantidade": qtd,
                                "total": total_item
                            })
                            st.rerun()
                    st.markdown("<hr style='margin: 8px 0px; border-color: #eee;'>", unsafe_allow_html=True)

        with st.expander("🥐 Salgados", expanded=False):
            renderizar_categoria(cat_salgados, "salgado")
            
        with st.expander("🍹 Sucos, Cremes e Açaís", expanded=False):
            renderizar_categoria(cat_sucos_acai, "suco")
            
        with st.expander("🥤 Bebidas e Cafés", expanded=False):
            renderizar_categoria(cat_bebidas_cafes, "outros")

    with col_pedido:
        st.subheader("📝 Pedido Atual")
        
        if not st.session_state.carrinho:
            st.info("Nenhum item adicionado a este pedido.")
        else:
            total_pedido = 0
            for index, item in enumerate(st.session_state.carrinho):
                col_item_txt, col_btn_excluir = st.columns([4, 1])
                
                with col_item_txt:
                    st.markdown(f"**{item['quantidade']}x** {item['produto']} — *R$ {item['total']:.2f}*")
                    total_pedido += item['total']
                    
                with col_btn_excluir:
                    if st.button("🗑️", key=f"del_{index}_{item['produto']}"):
                        st.session_state.carrinho.pop(index)
                        st.rerun()
            
            st.markdown("---")
            st.markdown(f"### 🧾 Total do Pedido: **R$ {total_pedido:.2f}**")
            
            col_finalizar, col_cancelar = st.columns(2)
            with col_finalizar:
                if st.button("✅ Registrar Venda", use_container_width=True, type="primary"):
                    operacoes.registrar_carrinho_no_banco(st.session_state.carrinho)
                    st.success("🎉 Venda registrada com sucesso!")
                    st.session_state.carrinho = []
                    st.rerun()
                    
            with col_cancelar:
                if st.button("❌ Cancelar Pedido", use_container_width=True):
                    st.session_state.carrinho = []
                    st.rerun()

# 📊 ATUALIZAÇÃO DA ABA DE RELATÓRIOS
with aba_historico:
    st.subheader("📊 Acompanhamento de Metas e Transações")
    
    # 1. Busca os faturamentos calculados pelo Pandas
    fat_diario, fat_mensal = operacoes.calcular_faturamento_periodo()
    
    # Criando duas colunas para destacar as metas de forma organizada
    m1, m2 = st.columns(2)
    with m1:
        st.metric(label="🎯 FATURAMENTO DIÁRIO (HOJE)", value=f"R$ {fat_diario:.2f}")
    with m2:
        st.metric(label="🏆 FATURAMENTO MENSAL ACUMULADO", value=f"R$ {fat_mensal:.2f}")
        
    st.markdown("---")
    
    # 2. Busca a planilha de vendas (já vindo invertida do operacoes.py)
    df_vendas = operacoes.obter_dataframe_vendas()
    
    if df_vendas.empty:
        st.info("Nenhuma venda registrada no arquivo CSV até o momento.")
    else:
        st.markdown("### 📋 Histórico Geral (Mais Recentes no Topo)")
        st.dataframe(df_vendas, use_container_width=True)