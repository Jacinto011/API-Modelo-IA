# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import base64
import pandas as pd
import numpy as np
from clustering_funcionarios import run_clustering
from predicao_funcionario import run_prediction
import threading
import matplotlib
matplotlib.use('Agg')  # Configura o backend para não interativo
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Garantir que a pasta static exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Lock para operações de arquivo
file_lock = threading.Lock()

def clean_dataframe_for_json(df):
    """Prepara um DataFrame para serialização JSON substituindo NaN/Inf por None"""
    df = df.replace([np.inf, -np.inf], np.nan)
    return df.where(pd.notnull(df), None)  # Faltava o parêntese de fechamento aqui

def image_to_base64(image_path):
    """Converte imagem para base64"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route('/')
def index():
    """Página inicial para testar a API"""
    return render_template('index.html')

@app.route('/api/clusterizar', methods=['GET', 'POST'])
def clusterizar():
    """Endpoint para executar a clusterização"""
    try:
        # Se for POST, verifica se há um novo arquivo
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dados_funcionarios.csv')
                file.save(file_path)
        
        # Executa a clusterização
        resultados, imagens = run_clustering()
        
        # Converte imagens para base64
        imagens_base64 = {}
        for nome, caminho in imagens.items():
            if os.path.exists(caminho):
                imagens_base64[nome] = image_to_base64(caminho)
        
        # Prepara resposta com tratamento de NaN
        clean_results = resultados.replace({np.nan: None}).to_dict(orient='records')
        
        response = {
            'status': 'success',
            'resultados': clean_results,
            'imagens': imagens_base64,
            'message': 'Clusterização realizada com sucesso'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/predizer', methods=['GET', 'POST'])
def predizer():
    """Endpoint para fazer predições"""
    try:
        # Se for POST, verifica se há um novo arquivo
        if request.method == 'POST' and 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dados_funcionarios.csv')
                file.save(file_path)
        
        # Verifica se é uma predição única ou em lote
        if request.method == 'POST' and request.json:
            # Predição única a partir dos dados enviados
            dados = request.json
            resultado = run_prediction(
                float(dados.get('Cumprimento Tarefas', 0)),
                float(dados.get('Assiduidade', 0)),
                float(dados.get('Pontualidade', 0)),
                float(dados.get('Comportamento', 0)),
                int(dados.get('Mês', 1))
            )
            
            # Garante que o resultado não contém NaN
            clean_result = {k: (None if v is None or (isinstance(v, float) and np.isnan(v)) else v) 
                          for k, v in resultado.items()}
            
            response = {
                'status': 'success',
                'resultado': clean_result,
                'message': 'Predição realizada com sucesso'
            }
        else:
            # Predição em lote (todo o dataset)
            resultados, imagens = run_prediction()
            
            # Converte imagens para base64
            imagens_base64 = {}
            for nome, caminho in imagens.items():
                if os.path.exists(caminho):
                    imagens_base64[nome] = image_to_base64(caminho)
            
            # Prepara resposta com tratamento de NaN
            clean_results = resultados.replace({np.nan: None}).to_dict(orient='records')
            
            response = {
                'status': 'success',
                'resultados': clean_results,
                'imagens': imagens_base64,
                'message': 'Predições realizadas com sucesso'
            }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/static/<filename>')
def uploaded_file(filename):
    """Endpoint para servir arquivos estáticos"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)