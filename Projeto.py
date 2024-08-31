import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold


# Leitura dos dados
dados = pd.read_csv("PPH 2019 - Banco de Dados V2.csv", delimiter=';', encoding='latin1', low_memory=False)

# Filtragem dos Dados por Estado
dataframes_estados = dict(tuple(dados.groupby('UF')))

# Escolha o estado de estudo
dadosUF = dataframes_estados["RJ"]
dadosUF.fillna(0, inplace=True)

colunas_selecionadas = [23, 50, 8, 11, 12, 13, 14, 15, 17, 1428, 1436, 1444, 1505, 1537, 1544, 1578, 1581, 1585, 
                        1588, 1591, 1594, 1597, 1600, 1603, 1606, 1609, 1612, 1615, 1618, 1621, 1624, 1627, 1631, 
                        1634, 1637, 1641, 1645, 1649, 1653, 1657, 1661, 1665, 1669, 1673, 1676, 1679, 1682, 1685, 
                        1688, 1691, 1694, 1697, 1700, 1703, 1706, 1735, 1764, 1792, 1820, 1848, 1877, 1906, 1935, 
                        1963, 1992, 2021, 2050, 2079, 2108, 2137, 2181, 2182, 21]
                        
dados_UF = dadosUF.iloc[:, colunas_selecionadas]
dados_UF = dados_UF.copy

# # # Alguns dados estão sendo lidos como string, por isso tem de ser convertidos para valores numéricos
# dados_UF['P3.1_4'] = dados_UF['P3.1_4'].astype(str).replace(',', '', regex=True).astype(float)
# dados_UF['P3.1_5'] = dados_UF['P3.1_5'].replace(',', '', regex=True).astype(float)
# dados_UF['P3.1_12'] = dados_UF['P3.1_12'].replace(',', '', regex=True).astype(float)
# dados_UF.loc[:, :] = dados_UF.fillna(0, inplace=True)

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

dados_UF_6classes = dados_UF

# Definir as condições e os valores correspondentes
conditions = [
    (dados_UF_6classes['CLASSE'] == 1),
    (dados_UF_6classes['CLASSE'] == 2),
    (dados_UF_6classes['CLASSE'] == 3),
    (dados_UF_6classes['CLASSE'] == 4),
    (dados_UF_6classes['CLASSE'] == 5),
    (dados_UF_6classes['CLASSE'] == 6)
]

values = ["A", "B1", "B2", "C1", "C2", "DE"]

# Criar a nova coluna 'CLASSE' com base nas condições
dados_UF_6classes['CLASSE'] = np.select(conditions, values, default=dados_UF_6classes['CLASSE'].astype(str))

proporcao_classes = dados_UF['CLASSE'].value_counts(normalize=True)
