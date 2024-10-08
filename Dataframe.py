import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import seaborn as sns
import matplotlib.pyplot as plt


# Leitura dos dados
dados = pd.read_csv("PPH 2019 - Banco de Dados V2.csv", delimiter=';', encoding='latin1', low_memory=False)

# Filtragem dos Dados por Estado
dataframes_estados = dict(tuple(dados.groupby('UF')))

# Escolha o estado de estudo
dadosUF = dataframes_estados["RJ"]
dadosUF.fillna(0, inplace=True)

#Renomeando Colunas
colunas_selecionadas = [23, 50, 8, 11, 12, 13, 14, 15, 17, 1428, 1436, 1444, 1505, 1537, 1544, 1578, 1581, 1585, 
                        1588, 1591, 1594, 1597, 1600, 1603, 1606, 1609, 1612, 1615, 1618, 1621, 1624, 1627, 1631, 
                        1634, 1637, 1641, 1645, 1649, 1653, 1657, 1661, 1665, 1669, 1673, 1676, 1679, 1682, 1685, 
                        1688, 1691, 1694, 1697, 1700, 1703, 1706, 1735, 1764, 1792, 1820, 1848, 1877, 1906, 1935, 
                        1963, 1992, 2021, 2050, 2079, 2108, 2137, 2181, 2182, 21]
                        
dados_UF = dadosUF.iloc[:, colunas_selecionadas]
dados_UF = dados_UF.copy()

# Preencher NaN com 0 em todo o DataFrame
dados_UF = dados_UF.fillna(0)

# Remover vírgulas e converter todas as colunas numéricas para float
dados_UF = dados_UF.apply(lambda x: x.astype(str).replace(',', '.', regex=True).astype(float) if x.dtype == 'object' else x)

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
# Identificar colunas duplicadas
duplicatas = dados_UF.columns[dados_UF.columns.duplicated()].unique()
# print(f"Colunas duplicadas: {duplicatas}")

# Obter nomes de colunas e verificar duplicados
colunas = dados_UF.columns
contagem = colunas.value_counts()
duplicadas = contagem[contagem > 1].index.tolist()

novos_nomes = []
nomes_contador = {nome: 1 for nome in duplicadas}

for nome in colunas:
    if nome in duplicadas:
        novos_nomes.append(f"{nome}_{nomes_contador[nome]}")
        nomes_contador[nome] += 1
    else:
        novos_nomes.append(nome)

dados_UF.columns = novos_nomes

dados_UF['Chuveiros_Eletricos'] = dados_UF.apply(lambda row: row['Chuveiros'] if row['Aquecimento_Chuveiro'] == 1 else 0, axis=1)

# Removendo Computador, Notebook, Lava Loucas, Secadora de Roupa e as Colunas do Chuveiro
dados_UF = dados_UF.drop(columns=[
    "Computador", "Notebook", "Secadora_de_Roupa", "Lava_Loucas_2", "Aquecimento_Chuveiro", "Chuveiros", "Maquina_de_Lavar_2", "Geladeiras_2",
      "Freezer_2", "Microondas_2"
])

# Visualizaçao dos Dados

# print(dados_UF.info())

print(dados_UF.head())

# Exportando os dados para csv
dados_UF.to_csv('dados.csv', index=False, sep=',')


# dados_UF_6classes = dados_UF.copy()

# # Definir as condições e os valores correspondentes
# conditions = [
#     (dados_UF_6classes['CLASSE'] == 1),
#     (dados_UF_6classes['CLASSE'] == 2),
#     (dados_UF_6classes['CLASSE'] == 3),
#     (dados_UF_6classes['CLASSE'] == 4),
#     (dados_UF_6classes['CLASSE'] == 5),
#     (dados_UF_6classes['CLASSE'] == 6)
# ]

# values = ["A", "B1", "B2", "C1", "C2", "DE"]

# # Criar a nova coluna 'CLASSE' com base nas condições
# dados_UF_6classes['CLASSE'] = np.select(conditions, values, default=dados_UF_6classes['CLASSE'].astype(str))

# proporcao_classes = dados_UF['CLASSE'].value_counts(normalize=True)

# # print(dados_UF_6classes.info())


# # #Verificando correlação entre os dados

# # # Calcula a matriz de correlação
# # corr_matrix = dados_UF.corr()

# # # Cria o gráfico de correlação
# # plt.figure(figsize=(8, 6))
# # sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0, square=True, linewidths=.5)
# # plt.show()



# #Análise Exploratória de cada Classe

# # Supondo que 'dados_UF' seja o seu DataFrame original

# # Criando DataFrames para cada classe
# df_classe_1 = dados_UF[dados_UF['CLASSE'] == 1]
# df_classe_2 = dados_UF[dados_UF['CLASSE'] == 2]
# df_classe_3 = dados_UF[dados_UF['CLASSE'] == 3]
# df_classe_4 = dados_UF[dados_UF['CLASSE'] == 4]
# df_classe_5 = dados_UF[dados_UF['CLASSE'] == 5]
# df_classe_6 = dados_UF[dados_UF['CLASSE'] == 6]

# # # Exibindo os primeiros registros de cada DataFrame para verificação
# # print(df_classe_1.head())
# # print(df_classe_2.head())
# # print(df_classe_3.head())
# # print(df_classe_4.head())
# # print(df_classe_5.head())
# # print(df_classe_6.head())


# # Criando boxplots de todas as variáveis no DataFrame
# plt.figure(figsize=(12, 8))
# sns.boxplot(data=df_classe_6)
# plt.xticks(rotation=90)  # Rotaciona os nomes das variáveis para caber no gráfico
# plt.show()
