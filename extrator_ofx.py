import pandas as pd
import os
from datetime import datetime

def extrair_dados_ofx():
    """
    Extrai dados de transações de arquivos OFX na pasta 'extratos'
    e retorna um DataFrame pandas com as transações.
    """
    df = pd.DataFrame()
    transactions_data = []
    
    # Verifica se a pasta extratos existe
    if not os.path.exists("extratos"):
        os.makedirs("extratos")
        return pd.DataFrame()
    
    # Lista todos os arquivos na pasta extratos
    for extrato in os.listdir("extratos"):
        if extrato.endswith('.ofx'):
            try:
                # Importa ofxparse apenas quando necessário
                import ofxparse
                
                # Abre e processa cada arquivo OFX
                with open(f'extratos/{extrato}', encoding='ISO-8859-1') as ofx_file:
                    ofx = ofxparse.OfxParser.parse(ofx_file)
                    
                    # Extrai as transações de cada conta
                    for account in ofx.accounts:
                        for transaction in account.statement.transactions:
                            transactions_data.append({
                                "Data": transaction.date,
                                "Valor": transaction.amount,
                                "Descrição": transaction.memo,
                                "Categoria": ""  # Será preenchido posteriormente
                            })
            except Exception as e:
                print(f"Erro ao processar arquivo {extrato}: {e}")
                continue
    
    # Converte a lista de transações em um DataFrame
    df_temp = pd.DataFrame(transactions_data)
    
    # Se houver transações, processa o DataFrame
    if not df_temp.empty:
        # Converte a coluna de data para o formato adequado
        df_temp['Data'] = pd.to_datetime(df_temp['Data']).dt.date
        
        # Ordena as transações por data
        df_temp = df_temp.sort_values(by='Data')
        
        df = df_temp
    
    return df

if __name__ == "__main__":
    # Testa a função de extração
    df_transacoes = extrair_dados_ofx()
    print(df_transacoes.head())
    print(f"Total de transações: {len(df_transacoes)}")

