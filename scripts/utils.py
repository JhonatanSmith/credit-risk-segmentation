import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def identificacion_categoricas_continuas(df, threshold:int, categoricas=[], continuas=[]):
    """
    Convierte columnas con un número de valores únicos menor o igual al umbral en variables categóricas y almacena los nombres de estas columnas. 
    También almacena los nombres de las columnas que se consideran continuas.

    Parámetros:
    df (DataFrame): El DataFrame de entrada.
    threshold (int): El número máximo de valores únicos para considerar una columna como categórica.
    categoricas (list): Lista para almacenar los nombres de las columnas categóricas.
    continuas (list): Lista para almacenar los nombres de las columnas continuas.

    Devuelve:
    df (DataFrame): El DataFrame con las columnas convertidas a categóricas.
    categoricas (list): Lista con los nombres de las columnas categóricas.
    continuas (list): Lista con los nombres de las columnas continuas.
    """
    for col in df.columns:
        if df[col].nunique() <= threshold:
            categoricas.append(col)
            df[col] = df[col].astype('category')
        else:
            continuas.append(col)
    return df, categoricas, continuas
        

def graficar_categoricas(df: pd.DataFrame, categorias: list, hue: str=None):
    """
    Grafica diagramas de barras y proporciones para una lista de variables categóricas.

    Esta función genera un gráfico de barras para cada variable categórica en la lista 
    `categorias`. Si se proporciona el argumento `hue`, se generan dos gráficos por variable: 
    uno que muestra las frecuencias absolutas (countplot) y otro que muestra las proporciones 
    relativas (histplot con 'multiple=fill'). Cada fila contiene los gráficos correspondientes 
    a una categoría.

    Args:
        categorias (list): Lista de nombres de columnas categóricas en el DataFrame `df`.
        hue (str, opcional): Nombre de una variable adicional para usar como desagregador 
                             en los gráficos. Por defecto es None.

    Returns:
        None: La función genera una figura con gráficos de barras y proporciones para 
              cada variable categórica, pero no devuelve ningún valor.
    
    Notas:
        - Si se pasa el parámetro `hue`, la figura tendrá dos gráficos por variable categórica: 
          uno con las frecuencias y otro con las proporciones relativas.
        - En caso contrario, solo se grafica el diagrama de barras con las frecuencias absolutas.
        - `plt.tight_layout()` se utiliza para evitar que los gráficos se superpongan.
    """
    if hue:
        fig, axs = plt.subplots(len(categorias), 2, figsize=(12, len(categorias) * 4))
        for i, categoria in enumerate(categorias):
            # Gráfico de barras con hue
            sns.countplot(data=df, x=categoria, ax=axs[i, 0], hue=hue)
            axs[i, 0].bar_label(axs[i, 0].containers[0])
            axs[i, 0].set_title(f'Diagrama de barras de {categoria}')
            axs[i, 0].set_xlabel(f'{categoria}')
            axs[i, 0].set_ylabel('Frecuencia')

            # Gráfico de proporciones
            sns.histplot(data=df, x=categoria, hue=hue, multiple='fill', stat='proportion', shrink=.8, ax=axs[i, 1])
            axs[i, 1].set_title(f'Proporción de {categoria} por {hue}')
            axs[i, 1].set_xlabel(f'{categoria}')
            axs[i, 1].set_ylabel('Proporción')

    else:
        fig, axs = plt.subplots(len(categorias), 1, figsize=(8, len(categorias) * 4))
        for i, categoria in enumerate(categorias):
            # Gráfico de barras sin hue
            sns.countplot(data=df, x=categoria, ax=axs[i])
            axs[i].bar_label(axs[i].containers[0])
            axs[i].set_title(f'Diagrama de barras de {categoria}')
            axs[i].set_xlabel(f'{categoria}')
            axs[i].set_ylabel('Frecuencia')

    plt.tight_layout()
    
def graficar_numericas(df: pd.DataFrame, numericas: list, hue: str=None):
    """
    Grafica histogramas y diagramas de caja para una lista de variables numéricas.

    Esta función genera, para cada variable numérica en la lista `numericas`, 
    dos gráficos en una fila: un histograma y un diagrama de caja (boxplot). 
    Los gráficos se crean utilizando Seaborn y muestran la distribución de 
    las variables.

    Args:
        numericas (list): Lista de nombres de columnas numéricas en el DataFrame `df`.
        hue (str, opcional): Nombre de una variable adicional para usar como desagregador 
                             en los gráficos. Por defecto es None.

    Returns:
        None: La función genera una figura con histogramas y diagramas de caja para 
              cada variable numérica, pero no devuelve ningún valor.
    
    Notas:
        - Cada fila de la figura contiene dos gráficos: un histograma y un diagrama de caja 
          para la misma variable numérica.
        - Se utiliza `plt.tight_layout()` para evitar que los gráficos se superpongan.
    """
    fig, axs = plt.subplots(len(numericas), 2, figsize=(12, len(numericas)* 4))

    for i, numerica in enumerate(numericas):
        sns.histplot(data=df, x=numerica, ax=axs[i, 0], hue=hue)
        axs[i, 0].set_title(f'Histograma de {numerica}')
        axs[i, 0].set_xlabel(f'{numerica}')
        axs[i, 0].set_ylabel('Frecuencia')
        
        sns.boxplot(data=df, x=numerica, ax=axs[i, 1], hue=hue)
        axs[i, 1].set_title(f'Diagrama de caja de {numerica}')
        axs[i, 1].set_xlabel(f'{numerica}')
        
    plt.tight_layout()
