import random
import csv
from itertools import islice

# Dados para geração aleatória
nomes = ["Ana", "Carlos", "Marta", "Pedro", "Sofia", "João", "Inês", "Miguel", "Beatriz", "Ricardo", 
         "Lúcia", "Hugo", "Catarina", "André", "Tânia", "Rui", "Cláudia", "Fernando", "Mariana", "António",
         "José", "Maria", "Luís", "Teresa", "Francisco", "Diana", "Paulo", "Laura", "Gonçalo", "Sara",
         "Manuel", "Filipa", "Bruno", "Raquel", "Nuno", "Patrícia", "Alexandre", "Helena", "Vítor", "Eduarda","Marcelo"]

sobrenomes = ["Silva", "Santos", "Fernandes", "Pereira", "Costa", "Rodrigues", "Martins", "Ferreira", 
              "Gomes", "Lopes", "Marques", "Alves", "Ribeiro", "Pinto", "Carvalho", "Teixeira", "Moreira",
              "Correia", "Mendes", "Nunes", "Soares", "Vieira", "Monteiro", "Cardoso", "Rocha", "Raposo",
              "Neves", "Coelho", "Cruz", "Baptista", "Machado", "Matos", "Azevedo", "Morais", "Barros", "Chicava", "Massango", "Manave", "Chapo", "Benjamim", "Machava", "Conceiao", "Albazine", "Machel"]

cargos = ["Recursos Humanos", "Técnico de Informática", "Técnico de Laboratório", "Assistente Financeiro",
          "Secretariado", "Diretor de Departamento", "Assistente Administrativo", "Analista de Dados",
          "Gestor de Projetos", "Consultor", "Engenheiro", "Designer", "Marketing", "Contabilista",
          "Supervisor", "Coordenador", "Auditor", "Assistente de Direção"]

meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", 
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

classificacoes = {
    (0, 4.9): "Insatisfatório",
    (5.0, 6.4): "Regular",
    (6.5, 7.9): "Bom",
    (8.0, 8.9): "Muito Bom",
    (9.0, 10): "Excelente"
}

def gerar_nota_final(assiduidade, pontualidade, cumprimento, comportamento):
    return round((assiduidade + pontualidade + cumprimento + comportamento) / 4, 2)

def obter_classificacao(nota):
    for intervalo, classificacao in classificacoes.items():
        if intervalo[0] <= nota <= intervalo[1]:
            return classificacao
    return "Sem classificação"

def gerar_funcionario(codigo):
    nome = random.choice(nomes) + " " + random.choice(sobrenomes)
    cargo = random.choice(cargos)
    ano = random.randint(2021, 2024)
    mes = random.choice(meses)
    
    # Gerar avaliações com distribuição mais realista
    assiduidade = min(10, max(0, int(random.gauss(9, 2))))
    pontualidade = min(10, max(0, int(random.gauss(8, 1.5))))
    cumprimento = min(10, max(0, int(random.gauss(8.5, 1.8))))
    comportamento = min(10, max(0, int(random.gauss(9, 1.2))))
    
    # Ajustar para que excelentes sejam mais raros
    if random.random() < 10:  # 90% de chance de reduzir pontuações muito altas
        assiduidade = min(9, assiduidade)
        pontualidade = min(7, pontualidade)
        cumprimento = min(9, cumprimento)
        comportamento = min(8, comportamento)
    
    nota_final = gerar_nota_final(assiduidade, pontualidade, cumprimento, comportamento)
    classificacao = obter_classificacao(nota_final)
    
    return [
        codigo, nome, cargo, ano, mes, assiduidade, pontualidade,
        cumprimento, comportamento, nota_final, classificacao
    ]

# Gerar 1000 registros
registros = []
for i in range(5000):
    codigo = 1 + i
    registros.append(gerar_funcionario(codigo))

# Escrever para CSV
with open('static/avaliacoes_funcionarios.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Codigo","Nome","Cargo","Ano","Mês","Assiduidade",
                    "Pontualidade","Cumprimento Tarefas","Comportamento",
                    "Nota Final","Classificação"])
    writer.writerows(registros)

# Mostrar os primeiros 20 registros como exemplo
for registro in islice(registros, 20):
    print(registro)