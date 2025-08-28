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

#Verificando as divergências
divergencias = []
datas = pd.unique(registros['data'].tolist() + negociacoes['data'].tolist())

for data in datas:
    try:
        reg_row = registros[registros['data'] == data].iloc[0]
        neg_row = negociacoes[negociacoes['data'] == data].iloc[0]
        col_div = [col for col in registros.columns if reg_row[col] != neg_row[col]]
        if col_div:
            divergencias.append({
                'data': data,
                'registros': reg_row.to_dict(),
                'negociacoes': neg_row.to_dict(),
                'colunas_divergentes': ','.join(col_div)
            })
    except Exception:
        divergencias.append({
            'data': data,
            'registros': data in registros['data'].values,
            'negociacoes': data in negociacoes['data'].values,
            'colunas_divergentes': ''
        })

divergencias_df = pd.DataFrame(divergencias)
print(divergencias_df)
divergencias_df.to_csv('files/Divergencias_Negociacoes_BCPSA4.csv', sep=';', index=False)