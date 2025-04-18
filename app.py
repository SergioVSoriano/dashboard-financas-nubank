import streamlit as st
import pandas as pd
from extrator_ofx import extrair_dados_ofx
from categorizador import categorizar_transacoes

# Função principal
def main():
    st.title("Dashboard de Finanças Pessoais")
    
    # Carregar os dados do arquivo OFX
    ofx_file_path = 'extratos/Nubank_2025-04-07.ofx'  # Certifique-se de que o caminho esteja correto
    df = extrair_dados_ofx(ofx_file_path)
    
    # Verifique se o DataFrame não está vazio
    if df.empty:
        st.error("Erro ao carregar os dados. Verifique o arquivo OFX.")
        return
    
    # Categorizar as transações
    df = categorizar_transacoes(df)
    
    # Exibir o DataFrame resultante no Streamlit
    st.write(df)

# Iniciar o Streamlit
if __name__ == "__main__":
    main()


