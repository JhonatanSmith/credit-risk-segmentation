
# preprocessing.py
import janitor
import pandas as pd
from utils import identificacion_categoricas_continuas, cambio_nombres, correcion_positivos

# Cargar los archivos
train_data = pd.read_csv("../data/raw/base_train.csv", sep="|")
valid_data = pd.read_csv("../data/raw/base_validacion.csv", sep="|")
test_data = pd.read_csv("../data/raw/base_prueba.csv", sep="|")

# Diccionario para almacenar los datos
data = {'train': train_data, 'valid': valid_data, 'test': test_data}

# Aplicar la función de cambio de nombres a cada DataFrame
data['train'] = cambio_nombres(data['train'])
data['valid'] = cambio_nombres(data['valid'])
data['test'] = cambio_nombres(data['test'])

# Separar variables categóricas y continuas para el conjunto de entrenamiento
data['train'], categoricas, continuas = identificacion_categoricas_continuas(df=data['train'], threshold=15)

for key in data.keys():
    # Estandarizar nombres de columnas manualmente
    data[key] = janitor.clean_names(data[key])
    # Corregir los valores positivos para las variables continuas
    data[key] = correcion_positivos(data[key], continuas, key)

# Guardar los DataFrames procesados en la carpeta "processed"
data['train'].to_csv("../data/processed/train_processed.csv", index=False)
data['valid'].to_csv("../data/processed/valid_processed.csv", index=False)
data['test'].to_csv("../data/processed/test_processed.csv", index=False)
