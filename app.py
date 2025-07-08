# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import csv
import io
import base64
import pandas as pd
import numpy as np
from clustering_funcionarios import run_clustering
import threading
import matplotlib
matplotlib.use('Agg')  # Configura o backend para não interativo
from flask_cors import CORS
from feedback import gerar_feedback_individual, processar_csv, gerar_feedback_por_dados
from datetime import datetime
from flask import Flask, request, jsonify
import joblib


# Carregar modelo e encoders
model = joblib.load('model/employee_performance_model.pkl')
le_mes = joblib.load('model/month_encoder.pkl')
le_cargo = joblib.load('model/role_encoder.pkl')

# Mapeamento de notas para classificação
def get_classification(nota):
    if nota >= 8:
        return "Muito Bom"
    elif nota >= 7:
        return "Bom"
    elif nota >= 6:
        return "Regular"
    else:
        return "Insuficiente"

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



@app.route('/api/predizer', methods=['POST'])
def predict_performance():
   
    try:
        data = request.json
        
        # Obter valores do request
        task_completion = float(data.get('Cumprimento de Tarefas', 0))
        attendance = float(data.get('Assiduidade', 0))
        punctuality = float(data.get('Pontualidade', 0))
        behavior = float(data.get('Comportamento', 0))
        current_month = data.get('Mes', 'janeiro')  # default janeiro
        prediction_months = int(data.get('MesesPrevisao', 3))
        
        # Criar dataframe para previsão
        predictions = []
        current_year = datetime.now().year
        
        # Simular previsão para os próximos meses
        for i in range(prediction_months):
            # Calcular próximo mês (simplificado)
            month_index = (le_mes.transform([current_month])[0] + i) % 12
            next_month = le_mes.inverse_transform([month_index])[0]
            
            # Usar cargo genérico (poderia ser passado no request)
            role = 'Recursos Humanos'
            
            # Preparar features
            features = pd.DataFrame({
                'Assiduidade': [attendance],
                'Pontualidade': [punctuality],
                'Cumprimento Tarefas': [task_completion],
                'Comportamento': [behavior],
                'Ano': [current_year],
                'Mês': [month_index],
                'Cargo': [le_cargo.transform([role])[0]]
            })
            
            # Fazer previsão
            predicted_score = model.predict(features)[0]
            classification = get_classification(predicted_score)
            
            predictions.append({
                'mes': next_month,
                'notaPrevista': round(float(predicted_score), 2),
                'classificacaoPrevista': classification
            })
        
        # Calcular nota atual (usando o mês atual)
        current_features = pd.DataFrame({
            'Assiduidade': [attendance],
            'Pontualidade': [punctuality],
            'Cumprimento Tarefas': [task_completion],
            'Comportamento': [behavior],
            'Ano': [current_year],
            'Mês': [le_mes.transform([current_month])[0]],
            'Cargo': [le_cargo.transform([role])[0]]
        })
        
        current_score = model.predict(current_features)[0]
        
        response = {
            "success": True,
            "data": {
                "predicoes": predictions,
                "notaAtual": round(float(current_score), 2),
                "classificacaoAtual": get_classification(current_score)
            }
        }
        print(response)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Erro ao processar a predição"
        }), 500
  

@app.route('/api/feedback/funcionario', methods=['POST'])
def post_feedback_funcionario():
    """Endpoint para gerar feedback a partir dos dados enviados no body JSON"""
    try:
        dados_funcionario = request.get_json()
        print(dados_funcionario)

        if not dados_funcionario:
            return jsonify({
                'status': 'error',
                'message': 'Nenhum dado JSON recebido no corpo da requisição'
            }), 400

        resultado = gerar_feedback_por_dados(dados_funcionario)

        if resultado.get('status') == 'error':
            return jsonify(resultado), 400

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/feedback/funcionario/<codigo>', methods=['GET'])
def get_feedback_funcionario(codigo):
    """Endpoint para obter feedback de um funcionário específico"""
    try:
        feedback = gerar_feedback_individual(codigo)
        
        if 'error' in feedback:
            return jsonify({'status': 'error', 'message': feedback['error']}), 404
        
        return jsonify({
            'status': 'success',
            'data': feedback,
            'message': 'Feedback gerado com sucesso'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/feedback/todos', methods=['GET'])
def get_all_feedbacks():
    """Endpoint para obter feedbacks de todos os funcionários"""
    try:
        feedbacks = processar_csv()
        
        if isinstance(feedbacks, dict) and 'error' in feedbacks:
            return jsonify({'status': 'error', 'message': feedbacks['error']}), 500
        
        return jsonify({
            'status': 'success',
            'data': feedbacks,
            'total': len(feedbacks),
            'message': 'Feedbacks coletados com sucesso'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/static/<filename>')
def uploaded_file(filename):
    """Endpoint para servir arquivos estáticos"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/atualizar_funcionarios', methods=['POST'])
def atualizar_funcionarios():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Nenhum arquivo enviado'}), 400

    arquivo_csv = request.files['file']

    if arquivo_csv.filename == '':
        return jsonify({'status': 'error', 'message': 'Arquivo sem nome'}), 400

    try:
        # Ler o CSV recebido na memória (em texto)
        stream = io.StringIO(arquivo_csv.stream.read().decode('utf-8'))
        novos_dados = list(csv.DictReader(stream))

        # Caminho do arquivo local
        arquivo_local = 'static/dados_funcionarios.csv'

        # Ler os dados atuais do arquivo local
        if os.path.exists(arquivo_local):
            with open(arquivo_local, mode='r', encoding='utf-8') as f:
                dados_atuais = list(csv.DictReader(f))
        else:
            dados_atuais = []

        # Transformar lista de dict em dict indexado pelo Codigo para facilitar atualização
        dados_dict = {func['Codigo'].strip(): func for func in dados_atuais}

        # Atualizar ou adicionar os dados recebidos
        for novo_func in novos_dados:
            codigo = novo_func.get('Codigo', '').strip()
            if codigo:
                dados_dict[codigo] = novo_func  # atualiza ou adiciona

        # Obter lista atualizada (valores do dict)
        dados_atualizados = list(dados_dict.values())

        # Campos do CSV — idealmente usar os campos do arquivo original ou do CSV recebido
        if dados_atualizados:
            campos = dados_atualizados[0].keys()
        else:
            return jsonify({'status': 'error', 'message': 'Nenhum dado válido para atualizar'}), 400

        # Escrever o arquivo CSV atualizado
        with open(arquivo_local, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(dados_atualizados)

        return jsonify({'status': 'success', 'message': 'Arquivo atualizado com sucesso'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erro ao processar arquivo: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)