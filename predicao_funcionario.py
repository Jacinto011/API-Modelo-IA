import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Carregar os dados
df = pd.read_csv('static/avaliacoes_funcionarios.csv')

# Pré-processamento
# Codificar meses e cargos
le_mes = LabelEncoder()
le_cargo = LabelEncoder()

df['Mês'] = le_mes.fit_transform(df['Mês'])
df['Cargo'] = le_cargo.fit_transform(df['Cargo'])

# Selecionar features e target
features = ['Assiduidade', 'Pontualidade', 'Cumprimento Tarefas', 'Comportamento', 'Ano', 'Mês', 'Cargo']
X = df[features]
y = df['Nota Final']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliar modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Salvar o modelo e os encoders
joblib.dump(model, 'model/employee_performance_model.pkl')
joblib.dump(le_mes, 'model/month_encoder.pkl')
joblib.dump(le_cargo, 'model/role_encoder.pkl')

print("Modelo treinado e salvo com sucesso!")