
# utils.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def identificacion_categoricas_continuas(df, threshold: int):
    """
    Convierte columnas con un número de valores únicos menor o igual al umbral en variables categóricas
    y almacena los nombres de estas columnas. También almacena los nombres de las columnas continuas.

    Parámetros:
    df (DataFrame): El DataFrame de entrada.
    threshold (int): El número máximo de valores únicos para considerar una columna como categórica.

    Devuelve:
    df (DataFrame): El DataFrame con las columnas convertidas a categóricas.
    categoricas (list): Lista con los nombres de las columnas categóricas.
    continuas (list): Lista con los nombres de las columnas continuas.
    """
    categoricas = []
    continuas = []
    for col in df.columns:
        if df[col].nunique() <= threshold:
            categoricas.append(col)
            df[col] = df[col].astype('category')
        else:
            continuas.append(col)
    return df, categoricas, continuas


def cambio_nombres(df):
    """
    Función para estandarizar el cambio de nombres de un DataFrame a nombres más descriptivos.
    """
    nombre_actual_a_nuevo = {
        "CO01ACP011RO": "cancel_pos_12m",
        "CO01ACP017CC": "meses_cancel_telcos",
        "CO01END002RO": "saldo_prom_rotativo",
        "CO01END010RO": "cupo_disp_rotativo",
        "CO01END051RO": "saldo_total_9_meses_rotativo",
        "CO01END086RO": "uso_total_prod_3m_rotativo",
        "CO01END094RO": "cupo_max_rotativo",
        "CO01EXP001CC": "meses_apertura_telcos",
        "CO01EXP002AH": "meses_apertura_ahorro",
        "CO01EXP003RO": "meses_apertura_rotativo",
        "CO01MOR098RO": "ponderacion_24m_rotativo",
        "CO01NUM002AH": "productos_abiertos_ahorro",
        "CO02END015CC": "porcentaje_cartera_vencida_telcos",
        "CO02EXP004TO": "meses_apertura_ultimo_prod_total",
        "CO02EXP011TO": "porcentaje_productos_48meses_total",
        "CO02MOR092TO": "ponderacion_reportes_al_dia_18m_total",
        "CO02NUM043RO": "pct_productos_cerrados_rotativo",
        "CO02NUM086AH": "part_ahorro_total",
        "disp309": "version_sistema_operativo",
        "trx102": "monto_min_transado_1m",
        "trx106": "monto_min_transado_2m",
        "trx143": "desv_recargas_pse_12m",
        "trx158": "prom_retiros_atm_12m",
        "trx39": "desv_retiros_atm_12m",
        "num_doc": "id_cliente",
        "f_analisis": "fecha_desembolso",
        "default": "incumplimiento",
        "tipo_cliente": "tipo_cliente"
    }
    print('ANTES DE CAMBIO DE NOMBRES')
    print(df.columns)
    df2 = df.rename(columns=nombre_actual_a_nuevo, inplace=False)
    print('DESPUES DE CAMBIO DE NOMBRES')
    print(df2.columns)
    return df2


def correcion_positivos(df, continuas: list, nombre_df: str):
    """
    Esta función corrige los valores positivos de las variables numéricas en el DataFrame de pandas.

    Args:
        df: Pandas DataFrame
        continuas: Lista con los nombres de columnas que contienen valores numéricos
    """
    print('DIMENSION DATAFRAME {}'.format(nombre_df), df.shape)
    df_filtrada = df[(df[continuas] >= 0).all(axis=1)]
    print('DIMENSION DATAFRAME {} DESPUES DE FILTRO'.format(nombre_df), df_filtrada.shape)
    return df_filtrada


def graficar_categoricas(df: pd.DataFrame, categorias: list, hue: str = None):
    """
    Grafica diagramas de barras y proporciones para una lista de variables categóricas.

    Args:
        df (DataFrame): DataFrame que contiene los datos.
        categorias (list): Lista con los nombres de las columnas categóricas.
        hue (str, opcional): Variable adicional para desagregar los gráficos.
    """
    if hue:
        fig, axs = plt.subplots(len(categorias), 2, figsize=(12, len(categorias) * 4))
        for i, categoria in enumerate(categorias):
            sns.countplot(data=df, x=categoria, ax=axs[i, 0], hue=hue)
            axs[i, 0].bar_label(axs[i, 0].containers[0])
            axs[i, 0].set_title(f'Diagrama de barras de {categoria}')
            axs[i, 0].set_xlabel(categoria)
            axs[i, 0].set_ylabel('Frecuencia')

            sns.histplot(data=df, x=categoria, hue=hue, multiple='fill', stat='proportion', shrink=.8, ax=axs[i, 1])
            axs[i, 1].set_title(f'Proporción de {categoria} por {hue}')
            axs[i, 1].set_xlabel(categoria)
            axs[i, 1].set_ylabel('Proporción')
    else:
        fig, axs = plt.subplots(len(categorias), 1, figsize=(8, len(categorias) * 4))
        for i, categoria in enumerate(categorias):
            sns.countplot(data=df, x=categoria, ax=axs[i])
            axs[i].bar_label(axs[i].containers[0])
            axs[i].set_title(f'Diagrama de barras de {categoria}')
            axs[i].set_xlabel(categoria)
            axs[i].set_ylabel('Frecuencia')

    plt.tight_layout()
    plt.show()


def graficar_numericas(df: pd.DataFrame, numericas: list, hue: str = None):
    """
    Grafica histogramas y diagramas de caja para una lista de variables numéricas.

    Args:
        df (DataFrame): DataFrame que contiene los datos.
        numericas (list): Lista con los nombres de las columnas numéricas.
        hue (str, opcional): Variable adicional para desagregar los gráficos.
    """
    fig, axs = plt.subplots(len(numericas), 2, figsize=(12, len(numericas) * 4))

    for i, numerica in enumerate(numericas):
        sns.histplot(data=df, x=numerica, ax=axs[i, 0], hue=hue)
        axs[i, 0].set_title(f'Histograma de {numerica}')
        axs[i, 0].set_xlabel(numerica)
        axs[i, 0].set_ylabel('Frecuencia')

        sns.boxplot(data=df, x=numerica, ax=axs[i, 1], hue=hue)
        axs[i, 1].set_title(f'Diagrama de caja de {numerica}')
        axs[i, 1].set_xlabel(numerica)

    plt.tight_layout()
    plt.show()


def balanceo_categorias(df):
    '''
    Funcion para balancear la categoria introducida por el sesgo asociado a 
    la variable 'tipo_cliente' en un dataframe.
    '''
    objetivo = df[df['tipo_cliente'] == 'objetivo']
    adicion = df[df['tipo_cliente'] == 'adicion']
    n =  int(np.ceil(0.5*objetivo.shape[0]))
    muestra = adicion.sample(n, random_state=1998)
    return pd.concat([objetivo, muestra])