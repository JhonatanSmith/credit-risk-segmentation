# External libraries
import pandas as pd
import numpy as np
import janitor
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Features engineersing
from sklearn.preprocessing import StandardScaler

# Lasso regression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
scaler = StandardScaler()
# Hiperparametros de Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso

# Own libraries
sys.path.append(os.path.abspath("../scripts"))
import utils


# reading files
test = pd.read_csv('../data/processed/test_processed.csv')
train = pd.read_csv('../data/processed/train_processed.csv')
train, categoricas, continuas = utils.identificacion_categoricas_continuas(train, threshold=15)

# External libraries
import pandas as pd
import numpy as np
import janitor
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Features engineering
from sklearn.preprocessing import StandardScaler

# Lasso regression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
scaler = StandardScaler()
# Hiperparámetros de Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso

# Own libraries
sys.path.append(os.path.abspath("../scripts"))
import utils

# Reading files
test = pd.read_csv('../data/processed/test_processed.csv')
train = pd.read_csv('../data/processed/train_processed.csv')

# Llamar a la función
train, categoricas, continuas = utils.identificacion_categoricas_continuas(train, threshold=15)

# **Eliminar 'incumplimiento' de las listas de variables**
if 'incumplimiento' in categoricas:
    categoricas.remove('incumplimiento')
if 'incumplimiento' in continuas:
    continuas.remove('incumplimiento')

def variable_selection(train, test, categoricas, continuas):
    # Combinar variables categóricas y continuas
    variables_seleccionadas = categoricas + continuas

    # Extraer las columnas seleccionadas del conjunto de entrenamiento y prueba
    X_train = train[variables_seleccionadas]
    y_train = train['incumplimiento']  # 'incumplimiento' es la variable objetivo
    X_test = test[variables_seleccionadas]
    y_test = test['incumplimiento'] if 'incumplimiento' in test.columns else None  # Puede que no tengas la variable objetivo en test

    # Aplicar one-hot encoding a las variables categóricas
    X_train_encoded = pd.get_dummies(X_train, columns=categoricas, drop_first=True)
    X_test_encoded = pd.get_dummies(X_test, columns=categoricas, drop_first=True)

    # Alinear las columnas de train y test después del one-hot encoding
    X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='left', axis=1, fill_value=0)

    # Escalar las variables
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_encoded)
    X_test_scaled = scaler.transform(X_test_encoded)

    # Definir rango de alphas para Lasso
    alpha_range = {'alpha': np.logspace(-4, 4, 100)}
    lasso_model = Lasso()

    # Búsqueda de cuadrícula para el mejor alpha
    grid_search = GridSearchCV(lasso_model, param_grid=alpha_range, cv=5)
    grid_search.fit(X_train_scaled, y_train)

    # Mejor valor de alpha
    best_alpha = grid_search.best_params_['alpha']
    print("Best alpha value used:", best_alpha)

    # Ajustar Lasso con el mejor alpha
    lasso_best = Lasso(alpha=best_alpha)
    lasso_best.fit(X_train_scaled, y_train)

    # Obtener coeficientes
    lasso_best_coef = pd.Series(lasso_best.coef_, index=X_train_encoded.columns)
    lasso_best_coef_sorted = lasso_best_coef[lasso_best_coef != 0].sort_values(ascending=False)

    # Imprimir variables seleccionadas por Lasso
    print("Por Regresión Lasso, las variables seleccionadas son:")
    print(lasso_best_coef_sorted)

    # Crear dataframe con variables seleccionadas por Lasso
    selected_features_lasso = lasso_best_coef_sorted.index.tolist()
    train_lasso = X_train_encoded[selected_features_lasso].copy()
    train_lasso['incumplimiento'] = y_train  # Añadir variable objetivo
    test_lasso = X_test_encoded[selected_features_lasso].copy()
    if y_test is not None:
        test_lasso['incumplimiento'] = y_test  # Añadir variable objetivo si existe

    # Exportar dataframes de Lasso a CSV
    train_lasso.to_csv('../data/model/train_Lasso.csv', index=False)
    test_lasso.to_csv('../data/model/test_Lasso.csv', index=False)
    print("\nArchivos 'train_Lasso.csv' y 'test_Lasso.csv' exportados con las variables seleccionadas por Lasso.")

    # Análisis PCA
    from sklearn.decomposition import PCA

    # Ajustar PCA en los datos escalados de entrenamiento
    pca = PCA()
    pca.fit(X_train_scaled)

    # Calcular la varianza acumulada explicada
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)

    # Determinar el número de componentes que explican el 90% de la varianza
    n_components_90 = np.argmax(cumulative_variance >= 0.90) + 1
    print(f"\nNúmero de componentes PCA para explicar el 90% de la varianza: {n_components_90}")

    # Reducir dimensionalidad con PCA
    pca = PCA(n_components=n_components_90)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)

    # Crear dataframes con componentes principales
    columns_pca = [f'PC{i+1}' for i in range(n_components_90)]
    train_pca = pd.DataFrame(X_train_pca, columns=columns_pca)
    train_pca['incumplimiento'] = y_train  # Añadir variable objetivo
    test_pca = pd.DataFrame(X_test_pca, columns=columns_pca)
    if y_test is not None:
        test_pca['incumplimiento'] = y_test  # Añadir variable objetivo si existe

    # Exportar dataframes de PCA a CSV
    train_pca.to_csv('../data/model/train_PCA.csv', index=False)
    test_pca.to_csv('../data/model/test_PCA.csv', index=False)
    print("Archivos 'train_PCA.csv' y 'test_PCA.csv' exportados con los componentes principales seleccionados por PCA.")

    # (Opcional) Mostrar las cargas de las variables en los componentes principales
    components = pd.DataFrame(pca.components_, columns=X_train_encoded.columns)
    for i in range(n_components_90):
        component = components.iloc[i]
        top_variables = component.abs().sort_values(ascending=False).head(10)
        print(f"\nPrincipales variables que contribuyen al componente principal {i+1}:")
        print(top_variables)

# Llamar a la función con los conjuntos de datos y listas de variables
variable_selection(train, test, categoricas, continuas)
