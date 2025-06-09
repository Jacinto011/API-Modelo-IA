# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib
matplotlib.use('Agg')  # Configura o backend para não interativo
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Verifica se o modelo já foi treinado e salvo
MODEL_PATH = 'static/modelo_funcionarios.pkl'

def clean_numeric_data(series, min_val=0, max_val=10):
    """Limpa e normaliza dados numéricos"""
    series = pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='coerce')
    series = np.clip(series, min_val, max_val)
    return series

def train_model():
    """Treina e salva o modelo de predição"""
    try:
        print("📊 CARREGANDO DADOS...")
        df = pd.read_csv('static/dados_funcionarios.csv', encoding='utf-8')
        
        # Converter e limpar colunas numéricas (0-10)
        numeric_cols = ['Assiduidade', 'Pontualidade', 'Cumprimento Tarefas', 'Comportamento', 'Nota Final']
        for col in numeric_cols:
            df[col] = clean_numeric_data(df[col])
        
        # Preencher valores ausentes após conversão
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Criar dados temporais se necessário
        if 'Mês' not in df.columns:
            df['Mês'] = np.random.randint(1, 13, size=len(df))
        
        # Modelagem
        features = ['Cumprimento Tarefas', 'Assiduidade', 'Pontualidade', 'Comportamento', 'Mês']
        target = 'Nota Final'
        
        X = df[features]
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=200, max_depth=6, random_state=42)
        model.fit(X_train, y_train)
        
        # Salva o modelo
        joblib.dump(model, MODEL_PATH)
        
        return model
    except Exception as e:
        print(f"Erro durante o treinamento do modelo: {str(e)}")
        raise e

def get_model():
    """Obtém o modelo (treina se necessário)"""
    try:
        if os.path.exists(MODEL_PATH):
            try:
                return joblib.load(MODEL_PATH)
            except:
                return train_model()
        else:
            return train_model()
    except Exception as e:
        print(f"Erro ao obter o modelo: {str(e)}")
        raise e

def run_prediction(ct=None, ass=None, pon=None, com=None, mes=None):
    """Executa predições - pode ser em lote ou única"""
    try:
        model = get_model()
        
        # Se todos os parâmetros forem fornecidos, faz uma predição única
        if all(v is not None for v in [ct, ass, pon, com, mes]):
            # Garante que os valores são numéricos
            ct = float(ct) if ct is not None else 0
            ass = float(ass) if ass is not None else 0
            pon = float(pon) if pon is not None else 0
            com = float(com) if com is not None else 0
            mes = int(mes) if mes is not None else 1
            
            input_data = pd.DataFrame([[ct, ass, pon, com, mes]],
                                    columns=['Cumprimento Tarefas', 'Assiduidade', 
                                            'Pontualidade', 'Comportamento', 'Mês'])
            predicao = model.predict(input_data)[0]
            predicao = np.clip(predicao, 0, 10)
            
            return {
                'Cumprimento Tarefas': ct,
                'Assiduidade': ass,
                'Pontualidade': pon,
                'Comportamento': com,
                'Mês': mes,
                'Nota_Prevista': round(float(predicao), 2),
                'Classificação': 'Alto Desempenho' if predicao >= 7 else 
                               'Desempenho Moderado' if predicao >= 5 else 
                               'Baixo Desempenho'
            }
        else:
            # Predição em lote (todo o dataset)
            df = pd.read_csv('static/dados_funcionarios.csv', encoding='utf-8')
            
            # Converter e limpar colunas numéricas (0-10)
            numeric_cols = ['Assiduidade', 'Pontualidade', 'Cumprimento Tarefas', 'Comportamento', 'Nota Final']
            for col in numeric_cols:
                df[col] = clean_numeric_data(df[col])
            
            # Preencher valores ausentes após conversão
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            
            # Criar dados temporais se necessário
            if 'Mês' not in df.columns:
                df['Mês'] = np.random.randint(1, 13, size=len(df))
            
            # Faz predições para os próximos 3 meses
            future_data = df.copy()
            future_data['Mês'] = (future_data['Mês'] + 3) % 12
            future_data['Mês'] = future_data['Mês'].replace(0, 12)
            future_data['Nota_Prevista'] = np.clip(model.predict(future_data[['Cumprimento Tarefas', 'Assiduidade', 
                                                                           'Pontualidade', 'Comportamento', 'Mês']]), 0, 10)
            
            # Garante que não há NaN nos resultados
            future_data['Nota_Prevista'] = future_data['Nota_Prevista'].fillna(0)
            
            # Gera gráficos
            plt.style.use('seaborn-v0_8')
            sns.set_theme(style="whitegrid")
            plt.rcParams['figure.figsize'] = (12, 6)
            
            # Gráfico de comparação Mês vs Previsão
            fig1, ax1 = plt.subplots(figsize=(14, 7))
            sns.lineplot(data=df, x='Mês', y='Nota Final', label='Desempenho Real', marker='o', ax=ax1)
            sns.lineplot(x=future_data['Mês'], y=future_data['Nota_Prevista'], 
                        label='Previsão Modelo', marker='o', linestyle='--', ax=ax1)
            ax1.set_title('Comparação: Desempenho Real vs Previsão por Mês', fontweight='bold')
            ax1.set_ylim(0, 10)
            ax1.axhline(y=5, color='r', linestyle=':', label='Mínimo Esperado')
            ax1.legend()
            ax1.grid(True)
            comparacao_img = 'static/comparacao_mes_previsao.png'
            fig1.savefig(comparacao_img, dpi=300)
            plt.close(fig1)
            
            # Importância das variáveis
            importance = pd.DataFrame({
                'Variável': ['Cumprimento Tarefas', 'Assiduidade', 'Pontualidade', 'Comportamento', 'Mês'],
                'Importância': model.feature_importances_
            }).sort_values('Importância', ascending=False)
            
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.barplot(data=importance, x='Importância', y='Variável', palette='rocket', ax=ax2)
            ax2.set_title('Importância das Variáveis no Modelo', fontweight='bold')
            plt.tight_layout()
            importancia_img = 'static/importancia_variaveis.png'
            fig2.savefig(importancia_img, dpi=300)
            plt.close(fig2)
            
            # Retorna resultados e caminhos das imagens
            imagens = {
                'comparacao_mes_previsao': comparacao_img,
                'importancia_variaveis': importancia_img
            }
            
            return future_data, imagens
    except Exception as e:
        print(f"Erro durante a predição: {str(e)}")
        raise e