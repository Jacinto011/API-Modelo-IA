# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use('Agg')  # Configura o backend para não interativo
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import os

def clean_numeric_data(series, min_val=0, max_val=10):
    """Limpa e normaliza dados numéricos"""
    series = pd.to_numeric(series.astype(str).str.replace(',', '.'), errors='coerce')
    series = np.clip(series, min_val, max_val)
    return series

def run_clustering():
    """Executa a análise de clusterização e retorna resultados e imagens"""
    try:
        # Configurações
        plt.style.use('seaborn-v0_8')
        sns.set_theme(style="whitegrid", palette="husl")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 11
        pd.set_option('display.max_columns', None)
        
        # 1. Carregar e preparar dados
        df = pd.read_csv('static/dados_funcionarios.csv', encoding='utf-8')
        
        # Converter e limpar colunas numéricas (0-10)
        numeric_cols = ['Assiduidade', 'Pontualidade', 'Cumprimento Tarefas', 'Comportamento', 'Nota Final']
        for col in numeric_cols:
            df[col] = clean_numeric_data(df[col])
        
        # Preencher valores ausentes após conversão
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # 2. Pré-processamento
        features = ['Assiduidade', 'Pontualidade', 'Cumprimento Tarefas', 'Comportamento']
        data = df[features].copy()
        
        # Preencher valores ausentes com a mediana
        imputer = SimpleImputer(strategy='median')
        data_imputed = imputer.fit_transform(data)
        
        # Normalização (0-1 para melhor visualização)
        scaler = MinMaxScaler(feature_range=(0, 10))
        data_scaled = scaler.fit_transform(data_imputed)
        
        # 3. Clusterização (K-Means com 5 clusters)
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=20)
        df['Cluster'] = kmeans.fit_predict(data_scaled)
        
        # 4. Definir perfis
        def definir_perfil(row):
            pontualidade_alta = df['Pontualidade'].quantile(0.75)
            pontualidade_baixa = df['Pontualidade'].quantile(0.25)
            produtividade_alta = df['Cumprimento Tarefas'].quantile(0.75)
            produtividade_baixa = df['Cumprimento Tarefas'].quantile(0.25)
            comportamento_alto = df['Comportamento'].quantile(0.75)
            assiduidade_baixa = df['Assiduidade'].quantile(0.25)
            
            if (row['Pontualidade'] >= pontualidade_alta) and (row['Cumprimento Tarefas'] <= produtividade_baixa):
                return "Pontual mas pouco produtivo"
            elif (row['Cumprimento Tarefas'] >= produtividade_alta) and (row['Assiduidade'] <= assiduidade_baixa):
                return "Produtivo mas irregular"
            elif (row['Comportamento'] >= comportamento_alto) and (row['Pontualidade'] <= pontualidade_baixa):
                return "Comprometido mas atrasado"
            elif all(row[feature] >= df[feature].quantile(0.75) for feature in features):
                return "Excelente em tudo"
            elif all(row[feature] <= df[feature].quantile(0.25) for feature in features):
                return "Precisa de acompanhamento"
            else:
                return "Desempenho regular"
        
        df['Perfil'] = df.apply(definir_perfil, axis=1)
        
        # Garantir que não há NaN nos resultados
        df['Perfil'] = df['Perfil'].fillna('Não classificado')
        df['Cluster'] = df['Cluster'].fillna(-1)
        
        # 5. Visualização dos Clusters (PCA)
        pca = PCA(n_components=2)
        data_pca = pca.fit_transform(data_scaled)
        
        fig1, ax1 = plt.subplots(figsize=(14, 8))
        scatter = sns.scatterplot(
            x=data_pca[:, 0], y=data_pca[:, 1],
            hue=df['Perfil'], palette="husl",
            s=100, style=df['Cluster'],
            alpha=0.9, edgecolor='black',
            ax=ax1
        )
        
        ax1.set_title('Clusterização de Desempenho dos Funcionários (0-10)', fontweight='bold', pad=20)
        ax1.set_xlabel('Componente Principal 1', fontsize=12)
        ax1.set_ylabel('Componente Principal 2', fontsize=12)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        cluster_img = 'static/cluster_desempenho.png'
        fig1.savefig(cluster_img, dpi=300, bbox_inches='tight')
        plt.close(fig1)
        
        # 6. Gráfico de distribuição das métricas
        fig2, ax2 = plt.subplots(2, 2, figsize=(14, 6))
        for i, col in enumerate(features):
            sns.histplot(df[col], bins=20, kde=True, ax=ax2[i//2, i%2])
            ax2[i//2, i%2].axvline(df[col].mean(), color='r', linestyle='--', label='Média')
            ax2[i//2, i%2].axvline(df[col].quantile(0.75), color='g', linestyle=':', label='P75')
            ax2[i//2, i%2].axvline(df[col].quantile(0.25), color='orange', linestyle=':', label='P25')
            ax2[i//2, i%2].set_title(f'Distribuição de {col} (0-10)')
            ax2[i//2, i%2].legend()
        plt.tight_layout()
        distribuicao_img = 'static/distribuicao_metricas.png'
        fig2.savefig(distribuicao_img, dpi=300)
        plt.close(fig2)
        
        # 7. Boxplot por Perfil
        fig3, ax3 = plt.subplots(figsize=(14, 8))
        order = sorted(df['Perfil'].unique())
        sns.boxplot(data=df, x='Perfil', y='Nota Final', palette="husl", 
                   order=order, showmeans=True, ax=ax3,
                   meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"black"})
        ax3.set_title('Distribuição das Notas Finais por Perfil (0-10)', fontweight='bold', pad=20)
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
        ax3.axhline(y=5, color='r', linestyle='--', alpha=0.5, label='Média Esperada (5)')
        ax3.legend()
        plt.tight_layout()
        boxplot_img = 'static/boxplot_desempenho.png'
        fig3.savefig(boxplot_img, dpi=300, bbox_inches='tight')
        plt.close(fig3)
        
        # 8. Heatmap de Correlação por Perfil
        cluster_means = df.groupby('Perfil')[features + ['Nota Final']].mean().round(2)
        cluster_means = cluster_means.fillna(0)  # Garante que não há NaN
        
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        sns.heatmap(cluster_means.T, annot=True, cmap="YlGnBu", fmt=".1f", 
                   linewidths=.5, vmin=0, vmax=10, cbar_kws={'label': 'Escala 0-10'}, ax=ax4)
        ax4.set_title('Média de Desempenho por Perfil (0-10)', fontweight='bold', pad=20)
        ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45)
        plt.tight_layout()
        heatmap_img = 'static/heatmap_perfis.png'
        fig4.savefig(heatmap_img, dpi=300, bbox_inches='tight')
        plt.close(fig4)
        
        # Retorna resultados e caminhos das imagens
        imagens = {
            'cluster_desempenho': cluster_img,
            'distribuicao_metricas': distribuicao_img,
            'boxplot_desempenho': boxplot_img,
            'heatmap_perfis': heatmap_img
        }
        
        return df, imagens
    
    except Exception as e:
        print(f"Erro durante a clusterização: {str(e)}")
        raise e