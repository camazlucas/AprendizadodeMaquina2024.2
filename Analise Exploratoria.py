import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
import seaborn as sns
import matplotlib.pyplot as plt

# Leitura dos dados
dados = pd.read_csv("dados.csv", delimiter=',', encoding='latin1', low_memory=False)

print(dados.info())

# Gerar dataframe para edição das classes
dados_6classes = dados.copy()

print(dados_6classes.info())


# Definir as classes numéricas para qualitativas
conditions = [
    (dados_6classes['CLASSE'] == 1),
    (dados_6classes['CLASSE'] == 2),
    (dados_6classes['CLASSE'] == 3),
    (dados_6classes['CLASSE'] == 4),
    (dados_6classes['CLASSE'] == 5),
    (dados_6classes['CLASSE'] == 6)
]

values = ["A", "B1", "B2", "C1", "C2", "DE"]


# Criar a nova coluna 'CLASSE' com base nas condições
dados_6classes['CLASSE'] = np.select(conditions, values, default=dados_6classes['CLASSE'].astype(str))

proporcao_classes = dados['CLASSE'].value_counts(normalize=True)


# print(dados_6classes.info())


# #Verificando correlação entre os dados

# # Calcula a matriz de correlação
# corr_matrix = dados_UF.corr()

# # Cria o gráfico de correlação
# plt.figure(figsize=(8, 6))
# sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0, square=True, linewidths=.5)
# plt.show()



#Análise Exploratória de cada Classe

# Supondo que 'dados_UF' seja o seu DataFrame original

# Criando DataFrames para cada classe
df_classe_A = dados[dados['CLASSE'] == 1]
df_classe_B1 = dados[dados['CLASSE'] == 2]
df_classe_B2 = dados[dados['CLASSE'] == 3]
df_classe_C1 = dados[dados['CLASSE'] == 4]
df_classe_C2 = dados[dados['CLASSE'] == 5]
df_classe_DE = dados[dados['CLASSE'] == 6]

# # Exibindo os primeiros registros de cada DataFrame para verificação
# print(df_classe_1.head())
# print(df_classe_2.head())
# print(df_classe_3.head())
# print(df_classe_4.head())
# print(df_classe_5.head())
# print(df_classe_6.head())


# Criando boxplots de todas as variáveis no DataFrame
plt.figure(figsize=(12, 8))
sns.boxplot(data=df_classe_A)
plt.xticks(rotation=90)  # Rotaciona os nomes das variáveis para caber no gráfico
plt.show()
