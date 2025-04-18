import os
import json

# Lista de categorias disponíveis
CATEGORIAS = [
    "Alimentação",
    "Receitas",
    "Saúde",
    "Mercado",
    "Educação",
    "Compras",
    "Transporte",
    "Investimento",
    "Transferências para terceiros",
    "Telefone",
    "Moradia"
]

def categorizar_transacao(descricao, valor):
    """
    Categoriza uma transação usando regras predefinidas
    """
    # Valores positivos são receitas
    if valor > 0:
        return "Receitas"
    
    # Regras para categorização baseadas em palavras-chave
    descricao_lower = descricao.lower()
    
    # Transferências
    if "pix" in descricao_lower and ("enviado" in descricao_lower or "transferido" in descricao_lower):
        return "Transferências para terceiros"
    
    # Transporte
    if any(keyword in descricao_lower for keyword in ["uber", "99app", "taxi", "recargapay", "cartvem", "passagem"]):
        return "Transporte"
    
    # Alimentação
    if any(keyword in descricao_lower for keyword in ["restaurante", "pizzaria", "burguer", "food", "supermercado", "bistro", "banca", "feira", "tomate", "frutas"]):
        return "Alimentação"
    
    # Saúde
    if any(keyword in descricao_lower for keyword in ["farmacia", "drogaria", "hospital", "clinica", "medico", "consulta"]):
        return "Saúde"
    
    # Educação
    if any(keyword in descricao_lower for keyword in ["escola", "curso", "livro", "educacao", "faculdade", "universidade"]):
        return "Educação"
    
    # Telefone
    if any(keyword in descricao_lower for keyword in ["telefone", "celular", "tim", "vivo", "claro", "oi", "operadora"]):
        return "Telefone"
    
    # Moradia
    if any(keyword in descricao_lower for keyword in ["aluguel", "condominio", "agua", "luz", "energia", "gas", "internet"]):
        return "Moradia"
    
    # Investimento
    if any(keyword in descricao_lower for keyword in ["investimento", "aplicacao", "tesouro", "bolsa", "acao", "fundo"]):
        return "Investimento"
    
    # Mercado
    if any(keyword in descricao_lower for keyword in ["mercado", "market", "atacado", "varejo"]):
        return "Mercado"
    
    # Compras (categoria padrão para despesas não identificadas)
    return "Compras"

def categorizar_transacoes(df):
    """
    Categoriza todas as transações no DataFrame
    """
    # Função para categorizar cada transação
    def categorizar_linha(row):
        if pd.isna(row['Categoria']) or row['Categoria'] == "":
            return categorizar_transacao(row['Descrição'], row['Valor'])
        return row['Categoria']
    
    # Aplica a função de categorização a cada linha
    df['Categoria'] = df.apply(categorizar_linha, axis=1)
    
    return df

def categorizar_manualmente(df, descricao, categoria):
    """
    Permite categorizar manualmente uma transação específica
    """
    # Encontra todas as linhas com a descrição fornecida
    mask = df['Descrição'].str.contains(descricao, case=False)
    
    # Atualiza a categoria para essas linhas
    if mask.any():
        df.loc[mask, 'Categoria'] = categoria
        print(f"Categorizado: {descricao} como {categoria}")
    else:
        print(f"Nenhuma transação encontrada com a descrição: {descricao}")
    
    return df

def salvar_categorias(df, arquivo='categorias.json'):
    """
    Salva as regras de categorização em um arquivo JSON
    """
    categorias = {}
    
    # Agrupa por descrição e categoria
    for _, row in df.iterrows():
        descricao = row['Descrição']
        categoria = row['Categoria']
        
        # Ignora descrições vazias
        if pd.isna(descricao) or descricao == "":
            continue
            
        # Adiciona ao dicionário
        categorias[descricao] = categoria
    
    # Salva no arquivo JSON
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(categorias, f, ensure_ascii=False, indent=4)
    
    print(f"Categorias salvas em {arquivo}")

def carregar_categorias(arquivo='categorias.json'):
    """
    Carrega as regras de categorização de um arquivo JSON
    """
    if not os.path.exists(arquivo):
        return {}
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        categorias = json.load(f)
    
    print(f"Categorias carregadas de {arquivo}")
    return categorias

def aplicar_categorias_salvas(df, categorias):
    """
    Aplica as categorias salvas ao DataFrame
    """
    # Para cada transação no DataFrame
    for i, row in df.iterrows():
        descricao = row['Descrição']
        
        # Se a descrição estiver nas categorias salvas, aplica a categoria
        if descricao in categorias:
            df.at[i, 'Categoria'] = categorias[descricao]
    
    return df
