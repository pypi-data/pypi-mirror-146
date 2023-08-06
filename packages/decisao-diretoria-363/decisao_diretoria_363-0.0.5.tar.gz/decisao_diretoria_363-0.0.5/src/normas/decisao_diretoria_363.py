#!/usr/bin/env python
# coding: utf-8

import os
import pprint
import pandas as pd
from collections import OrderedDict


def get_parameters():
    # Read Data
    try:
        df_363 = pd.read_excel(
            io=os.path.join(os.path.dirname(__file__), 'data', 'tab_dd_363.xlsx'),
            sheet_name='dd_363',
            index_col=0
        )
    except Exception as e:
        #print(e, '\n')
        #print('Read table from GitHub')
        df_363 = pd.read_excel(
            io='https://github.com/gaemapiracicaba/norma_dd_363_11/raw/main/src/normas/data/tab_dd_363.xlsx',
            sheet_name='dd_363',
            index_col=0
        )

    # Filter only quality
    df_363 = df_363.loc[(df_363['tipo_padrao'] == 'qualidade')]

    # Classes
    list_classes = list(set(df_363['padrao_qualidade']))
    list_classes = [x for x in list_classes if pd.notnull(x)]
    list_classes.sort()

    return df_363, list_classes


def filter_by_classe(df_363, classe):
    # Filter dataframe by Classe
    df_363 = df_363.loc[(df_363['padrao_qualidade'] == classe)]

    # Parâmetros
    list_parametros = list(set(df_363['parametro_descricao']))
    list_parametros = [x for x in list_parametros if pd.notnull(x)]
    list_parametros.sort()    
    return df_363, list_parametros


# def filter_by_parameters(df_363, parametro):
#     # Filter dataframe by Parametro
#     df_363 = df_363.loc[(df_363['parametro_descricao'] == parametro)]
#
#     # Check and Get Results
#     if len(df_363) == 1:
#         dict_363 = df_363.to_dict(orient='records')[0]
#         dict_363 = OrderedDict(sorted(dict_363.items(), key=lambda x: df_363.columns.get_loc(x[0])))
#         return dict_363
#     else:
#         return 'erro'


def filter_by_parameters(df_363, parametro, condicao=None):
    # Filter dataframe by Parametro
    df_363 = df_363.loc[(df_363['parametro_descricao'] == parametro)]

    # Condição
    array = df_363['condicao'].values
    dict_condicao = dict(enumerate(array.flatten(), 1))

    # Check and Get Results
    if len(df_363) == 1 and len(array) == 1:
        dict_363 = df_363.to_dict(orient='records')[0]
        dict_363 = OrderedDict(sorted(dict_363.items(), key=lambda x: df_363.columns.get_loc(x[0])))
        return dict_363

    elif len(df_363) > 1 and len(array) > 1 and condicao is not None:
        try:
            # Filtra a Condição
            #condicao = df_357['condicao'].values[condicao]
            df_363 = df_363.loc[(df_363['condicao'] == dict_condicao[int(condicao)])]
            dict_363 = df_363.to_dict(orient='records')[0]
            dict_363 = OrderedDict(sorted(dict_363.items(), key=lambda x: df_363.columns.get_loc(x[0])))
            return dict_363
        except Exception as e:
            #print(e)
            print('A condição definida foi "{}".\nAs opções possíveis são:\n'.format(condicao))
            print(*('{} - {}'.format(k, v) for k,v in dict_condicao.items()), sep='\n')

    else:
        print('Parâmetro "{}" tem mais de um registro.\nFaz-se necessário definir condição!\n'.format(parametro))
        print(*('{} - {}'.format(k, v) for k,v in dict_condicao.items()), sep='\n')


def set_type_desconformidade(dict_363):
    if pd.isnull(dict_363['valor_minimo_permitido']) & pd.notnull(dict_363['valor_maximo_permitido']):
        #print('Parâmetro só tem "valor máximo". Caso o valor medido esteja acima, é amostra desconforme!')
        tipo_363 = 'acima>desconforme'

    elif pd.notnull(dict_363['valor_minimo_permitido']) & pd.isnull(dict_363['valor_maximo_permitido']):
        #print('Parâmetro só tem "valor mínimo". Caso o valor medido esteja abaixo, é amostra desconforme!')
        tipo_363 = 'abaixo>desconforme'

    elif pd.notnull(dict_363['valor_minimo_permitido']) & pd.notnull(dict_363['valor_maximo_permitido']):
        #print('Parâmetro tem "valor mínimo" e "valor máximo". Caso o valor medido acima ou abaixo, é amostra desconforme!')
        tipo_363 = 'abaixo_acima>desconforme'

    elif pd.isnull(dict_363['valor_minimo_permitido']) & pd.isnull(dict_363['valor_maximo_permitido']):
        #print('Erro!')
        tipo_363 = 'erro'
    else:
        print('Erro!')
        #tipo_363 = 'erro'

    return tipo_363


def evaluate_result(valor, dict_363):
    # Get type
    tipo_363 = set_type_desconformidade(dict_363)

    # Evaluate type
    if tipo_363 == 'acima>desconforme':
        if valor > dict_363['valor_maximo_permitido']:
            result_363 = 'desconforme'
        else:
            result_363 = 'conforme'

    elif tipo_363 == 'abaixo>desconforme':
        if valor < dict_363['valor_minimo_permitido']:
            result_363 = 'desconforme'
        else:
            result_363 = 'conforme'

    elif tipo_363 == 'abaixo_acima>desconforme':
        if dict_363['valor_minimo_permitido'] <= valor <= dict_363['valor_maximo_permitido']:
            result_363 = 'conforme'
        else:
            result_363 = 'desconforme'

    else:
        result_363 = 'erro'

    return result_363




