#Importando as bibliotecas necessárias
import pandas as pd
from unidecode import unidecode

#Definido funções para reutilização
def normalizar_colunas(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.columns = df.columns.str.replace('¢', 'o').str.replace('£', 'u')
    df.columns = [unidecode(col) for col in df.columns]

#Importando os arquivos
registros = pd.read_csv('files/Registros_BCPSA4.csv', sep=',', encoding='latin1')
negociacoes = pd.read_csv('files/Negociacoes_BCPSA4.xls', sep='\t', encoding='latin1', skiprows=2)

#Filtrando as colunas de interesse
colunas = ['data', 'emissor', 'quantidade','numero_de_negocios']

normalizar_colunas(registros)
normalizar_colunas(negociacoes)

registros = registros[colunas]
negociacoes = negociacoes[colunas]

print(registros)
print(negociacoes)