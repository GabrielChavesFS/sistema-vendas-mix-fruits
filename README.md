# 🍇 Sistema de Vendas & Painel Gerencial — Mix Fruits

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

Uma aplicação web moderna de frente de caixa (PDV) e inteligência de negócios desenvolvida para otimizar a operação diária e o acompanhamento de metas financeiras de uma lanchonete real. 

O sistema foi desenhado focando em uma experiência de usuário (UX) simples e intuitiva para os operadores de caixa, eliminando interações complexas via terminal e automatizando o tratamento de dados.

---

## 🎯 Principais Funcionalidades

* **🛍️ Tela de Vendas (PDV Web):** Cardápio interativo e responsivo organizado por categorias dinâmicas (recolhidas por padrão para melhor usabilidade).
* **🛒 Comanda / Pedido Atual Dinâmico:** Sistema de retenção de itens em memória que permite o ajuste de quantidades individuais e a exclusão de itens antes da consolidação da venda, mitigando o erro humano.
* **⏱️ Análise de Séries Temporais:** Carimbo automático de data e hora (`YYYY-MM-DD HH:MM:SS`) para cada transação no banco de dados.
* **📊 Painel Gerencial Baseado em Metas:** Filtros dinâmicos que calculam e exibem de forma isolada o **Faturamento Diário (Reset automático à meia-noite)** e o **Faturamento Mensal Acumulado**, permitindo o acompanhamento de metas comerciais em tempo real.
* **🗂️ Histórico Compacto:** Exibição inteligente fixada apenas nas **10 transações mais recentes** para otimização de espaço e performance na tela principal, mantendo o histórico completo salvo no backend.

---

## 🛠️ Arquitetura e Estrutura do Projeto

O software foi construído seguindo os princípios de **Programação Modular**, garantindo a separação de responsabilidades e facilitando futuras expansões (como a transição planejada para Programação Orientada a Objetos):

* `banco_dados.py`: Centraliza o catálogo de produtos e a matriz de preços.
* `operacoes.py`: Camada de lógica de negócios e persistência. Responsável pelas operações aritméticas, manipulação de arquivos locais e aplicação de filtros booleanos do Pandas.
* `app.py`: Interface gráfica e gerenciamento de estado da aplicação (`st.session_state`) via Streamlit.

---

## 📈 Tecnologias e Conceitos Aplicados

* **Python (Fundamentos Avançados):** Estruturas de dados complexas (Dicionários aninhados, Listas de Compreensão) e modularização.
* **Pandas (Análise de Dados):**
    * Leitura e gravação eficiente de arquivos estruturados (`.csv`).
    * Ordenação de dados indexados por tempo (`sort_values`).
    * Manipulação de strings de tempo convertidas para objetos `datetime` nativos.
    * Cálculo de agregados e somatórios (`.sum()`).
    * Limitação de visualização de DataFrames utilizando exibições parciais (`.head()`).
* **Streamlit (Front-End & State Management):** Criação de layouts de alta fidelidade e persistência de dados em tempo de execução de página.

---

## 🚀 Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/GabrielChavesFS/sistema-vendas-mix-fruits.git](https://github.com/GabrielChavesFS/sistema-vendas-mix-fruits.git)
   cd sistema-vendas-mix-fruits