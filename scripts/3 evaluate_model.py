from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss, confusion_matrix, classification_report, roc_curve
import matplotlib.pyplot as plt
import pandas as pd
import joblib

train_lasso = pd.read_csv('../data/model/train_Lasso.csv')
test_lasso = pd.read_csv('../data/model/test_Lasso.csv')

X_train = train_lasso.drop('incumplimiento', axis=1)
y_train = train_lasso['incumplimiento']
X_test = test_lasso

valid_lasso = pd.read_csv('../data/processed/valid_processed.csv')
X_valid = valid_lasso.drop('incumplimiento', axis=1)
y_valid = valid_lasso['incumplimiento']
X_train, X_valid = X_train.align(X_valid, join='left', axis=1, fill_value=0)
log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train, y_train)
y_valid_pred = log_reg.predict(X_valid)
y_valid_proba = log_reg.predict_proba(X_valid)[:, 1]



# AUC-ROC
roc_auc = roc_auc_score(y_valid, y_valid_proba)
print(f"AUC-ROC: {roc_auc:.4f}")

# Log-Loss
logloss = log_loss(y_valid, y_valid_proba)
print(f"Log-Loss: {logloss:.4f}")

# Matriz de Confusión
cm = confusion_matrix(y_valid, y_valid_pred)
print("Matriz de Confusión:")
print(cm)

# Precision, Recall, F1-Score
print("Reporte de Clasificación:")
print(classification_report(y_valid, y_valid_pred))

#Serialización del modelo
joblib.dump(log_reg, '../models/log_reg_model.pkl')
print("Modelo serializado y guardado como 'log_reg_model.pkl'.")

importance = log_reg.coef_[0]
feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importance
})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

print("Variables más importantes con su coeficiente de importancia:")
print(feature_importance_df)

# Exportar las variables más importantes a un archivo CSV si es necesario
feature_importance_df.to_csv('../models/feature_importance_log_reg.csv', index=False)
def asignar_grupo_riesgo(probabilidad):
    if probabilidad <= 0.01:
        return 'T1'
    elif 0.01 < probabilidad <= 0.015:
        return 'T2'
    elif 0.015 < probabilidad <= 0.03:
        return 'T3'
    elif 0.03 < probabilidad <= 0.045:
        return 'T4'
    elif 0.045 < probabilidad <= 0.08:
        return 'T5'
    elif 0.08 < probabilidad <= 0.15:
        return 'T6'
    elif 0.15 < probabilidad <= 0.3:
        return 'T7'
    else:
        return 'T8'

valid_lasso['probabilidad_incumplimiento'] = y_valid_proba
valid_lasso['grupo_riesgo'] = valid_lasso['probabilidad_incumplimiento'].apply(asignar_grupo_riesgo)

print(valid_lasso[['probabilidad_incumplimiento', 'grupo_riesgo']].head())

print('VALUE COUNT POR GRUPO DE RIESGGO')
conteo_grupo_riesgo = valid_lasso['grupo_riesgo'].value_counts()

print("Conteo por grupo de riesgo:")
print(conteo_grupo_riesgo)

conteo_grupo_riesgo.to_csv('../data/model/conteo_grupos_riesgo.csv', index=False)
