import pandas as pd
import numpy as np

# Leitura dos dados
# dados = pd.read_csv("PPH 2019 - Banco de Dados V2.csv", delimiter=';', encoding='latin1', low_memory=False)
dados_UF = pd.read_csv("dadosfiltradosRJ.csv", delimiter=';', encoding='latin1', low_memory=False)
print(dados_UF.columns)

# # Alguns dados estão sendo lidos como string, por isso tem de ser convertidos para valores numéricos
dados_UF.loc[:, 'P3.1_4'] = dados_UF['P3.1_4'].replace(',', '', regex=True).astype(float)
dados_UF.loc[:, 'P3.1_5'] = dados_UF['P3.1_5'].replace(',', '', regex=True).astype(float)
dados_UF.loc[:, 'P3.1_12'] = dados_UF['P3.1_12'].replace(',', '', regex=True).astype(float)
dados_UF.fillna(0, inplace=True)
dados_UF = dados_UF.iloc[:, :-4]

# # Definindo os nomes das variáveis
nomesvariaveis = [
    "Qtd_Moradores", "Comercio", "Maquina_de_Lavar", "Geladeiras", "Freezer", "Microcomputador", "Lava_Loucas", "Microondas",
    "Secadora_de_Roupa", "Geladeiras", "Freezer", "Ar_Condicionado", "Televisao", "Microondas", "Maquina_de_Lavar", "Batedeira",
    "Cafereira", "Sanduicheira", "Espremedor", "Liquidificador", "Multiprocessador", "Panela_Eletrica", "Triturador_de_Lixo",
    "Faca_Eletrica", "Ebulidor", "Fogao_Eletrico", "Fritadeira_com_Oleo", "Fritadeira_sem_Oleo", "Enceradeira", "Aspirador_de_Po",
    "Panificadora", "DVD", "Tablet", "Celular", "Telefone_sem_Fio", "Fax", "Modem_Wifi", "Roteador_WIFI", "Impressora",
    "Receptor_de_TV", "Conversor_Digital", "Receptor_Digital", "NoBreak", "Serra_Eletrica", "Maquina_de_Solda", "Furadeira",
    "Portao_Eletronico", "Projetores", "Lava_Jato", "Filtro_de_Piscina", "Bomba_Dagua", "Maquina_de_Costura", "Chapinha",
    "Secador_de_Cabelo", "Forno_Eletrico", "Lava_Loucas", "Ferro_Eletrico_Seco", "Ferro_Eletrico_Vapor", "Ferro_Eletrico_sem_Vapor",
    "Secadora_Aquecimento", "Secadora_Centrifuga", "Aquecedor_de_Ambiente", "Ventilador_de_Teto", "Circulador_de_Ar", "Videogame",
    "Notebook", "Som_Radio", "Computador", "Filtro_de_Agua", "Adega", "Chuveiros", "Aquecimento_Chuveiro", "CLASSE"
]
dados_UF.columns = nomesvariaveis

# Removendo Residências que possuem atividade comercial
dados_UF = dados_UF[dados_UF['Comercio'] == 1]
dados_UF.drop(columns=['Comercio'], inplace=True)

# Removendo dados Duplicados
colunas_com_sufixos = [col for col in dados_UF.columns if '.' in col]
colunas_sem_sufixos = [col for col in dados_UF.columns if col not in colunas_com_sufixos]
dados_UF = dados_UF[colunas_sem_sufixos]
dados_UF['Chuveiros_Eletricos'] = dados_UF.apply(lambda row: row['Chuveiros'] if row['Aquecimento_Chuveiro'] == 1 else 0, axis=1)

# Removendo Computador, Notebook, Lava Loucas, Secadora de Roupa e as Colunas do Chuveiro
dados_UF = dados_UF.drop(columns=[
    "Computador", "Notebook", "Secadora_de_Roupa", "Lava_Loucas", "Aquecimento_Chuveiro", "Chuveiros"
])