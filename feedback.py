import random
import csv
from datetime import datetime

# Banco de frases ampliado com mais variações
BANCO_FRASES = {
    'saudacao': [
        "Olá, {nome}! Espero que você esteja bem e com energias renovadas.",
    "Prezado(a) {nome}, é um prazer compartilhar este feedback com você.",
    "Caro(a) {nome}, desejo que esta mensagem o(a) encontre bem.",
    "Oi {nome}, espero que seu mês tenha sido produtivo e inspirador!",
    "Querido(a) {nome}, receba esta mensagem com carinho e reconhecimento pelo seu esforço.",
    "Olá, {nome}! Que bom poder acompanhar sua jornada de crescimento conosco.",
    "Olá, {nome}! Que esta mensagem traga reconhecimento pelo seu desempenho.",
    "Saudações, {nome}. Esperamos que você esteja tendo um ótimo ciclo dia.",
    "Seja bem-vindo(a), {nome}, ao feedback mensal — um momento de reflexão e progresso.",
    "Olá, {nome}! Com alegria, iniciamos este momento de partilha sobre sua evolução recente."
    ],
    'introducao': [
            "Após avaliarmos cuidadosamente seu desempenho no mês de {mes}, gostaríamos de compartilhar as observações a seguir:",
    "Conforme a análise realizada para o mês de {mes}, segue abaixo o feedback com pontos de destaque e sugestões construtivas:",
    "Aqui está o retorno referente ao seu desempenho no mês de {mes}, elaborado com o objetivo de apoiar seu crescimento profissional:",
    "Segue a avaliação personalizada do mês de {mes}, com foco em reconhecer seus méritos e identificar oportunidades de melhoria:",
    "Com base nos dados coletados e na sua atuação ao longo do mês de {mes}, apresentamos a seguir uma análise detalhada:",
    "O mês de {mes} trouxe importantes insights sobre sua jornada profissional — e gostaríamos de partilhá-los com você.",
    "A seguir, apresentamos uma visão completa de sua atuação no período de {mes}, com foco no desenvolvimento contínuo.",
    "Trazemos um feedback referente a {mes}, com base em indicadores e observações práticas.",
    "Preparamos este retorno com base em sua atuação em {mes}, visando incentivar melhorias e valorizar conquistas.",
    "O mês de {mes} nos permitiu acompanhar sua evolução, e gostaríamos de compartilhar algumas reflexões."

    ],
    'elogio_geral': [
          "Parabéns! Seu desempenho foi classificado como {classificacao} (nota {nota}), demonstrando comprometimento e excelência.",
    "Excelente trabalho! Sua avaliação atingiu o nível {classificacao} (nota {nota}), o que reforça seu valor para a equipe.",
    "Resultado impressionante: {classificacao} (nota {nota}) — você superou as expectativas e merece reconhecimento.",
    "Seu desempenho alcançou o nível {classificacao} (nota {nota}), refletindo seu esforço e dedicação diária.",
    "Classificação {classificacao} (nota {nota}) — uma conquista notável que merece ser celebrada com entusiasmo!",
    "Você se destacou com uma nota {nota}, atingindo o nível {classificacao} — um resultado de grande mérito!",
    "Seu desempenho neste mês foi classificado como {classificacao} — parabéns pela consistência e comprometimento.",
    "Com a nota {nota}, você demonstrou um desempenho sólido e uma postura exemplar.",
    "Atingir a classificação {classificacao} é reflexo de um esforço contínuo — continue assim!",
    "Seu empenho foi claramente refletido em sua nota {nota}, classificada como {classificacao} — continue nesse caminho promissor."

    ],
    'elogio_pontos_fortes': [
     "Seus principais pontos fortes neste mês demonstraram seu crescimento e sua capacidade de entregar resultados consistentes:",
    "Destaques do seu desempenho que merecem reconhecimento e reforçam sua contribuição para a equipe:",
    "Áreas em que você se destacou de forma significativa, mostrando excelência e comprometimento:",
    "Pontos positivos que refletem sua competência e agregam valor ao time:",
    "Seus maiores acertos este mês merecem destaque, pois contribuíram diretamente para o sucesso coletivo:",
    "Estes foram os pilares do seu desempenho que mais se evidenciaram neste ciclo:",
    "Você apresentou um desempenho sólido em diversas frentes — eis os destaques:",
    "Os seguintes aspectos da sua atuação foram notadamente positivos e contribuíram para o bom andamento das atividades:",
    "Estes pontos fortes merecem ser reconhecidos como frutos da sua dedicação diária:",
    "Aqui estão os aspectos mais admirados na sua atuação durante o mês de {mes}:"

    ],
    'encorajamento': [
        "Continue com esse excelente trabalho e saiba que seu esforço está sendo notado e valorizado!",
    "Mantenha esse ritmo admirável, pois você está construindo uma trajetória de sucesso consistente.",
    "Siga nesse caminho promissor, pois os frutos do seu empenho continuarão a aparecer.",
    "Não mude essa postura positiva e comprometida — ela inspira os que estão à sua volta!",
    "Você está no caminho certo! Com essa dedicação, grandes conquistas virão.",
    "Seu desempenho tem sido motivo de orgulho — siga com essa motivação e energia!",
    "É animador ver sua evolução constante — continue buscando sua melhor versão.",
    "Seu progresso é evidente, e com foco você pode alcançar voos ainda maiores.",
    "A consistência com que você vem atuando é um grande diferencial — mantenha isso.",
    "Que seu exemplo continue a inspirar outros — sua jornada está sendo admirável!"
    ],
    'sugestao_melhoria': [
           "A seguir, apresentamos algumas sugestões que podem contribuir para seu desenvolvimento contínuo:",
    "Identificamos oportunidades que podem ser trabalhadas para elevar ainda mais seu desempenho:",
    "Apontamos abaixo alguns pontos que, com pequenos ajustes, podem impulsionar seus resultados:",
    "Essas áreas representam chances valiosas para crescimento e aperfeiçoamento profissional:",
    "Sugestões construtivas para sua evolução, elaboradas com o objetivo de fortalecer suas competências:",
    "É sempre possível evoluir — veja algumas observações que podem aprimorar ainda mais seu desempenho:",
    "Com foco e atenção, estas sugestões poderão alavancar sua performance nos próximos ciclos:",
    "As orientações a seguir foram pensadas com base no seu potencial de crescimento:",
    "Acreditamos que você pode ir além — considere estas dicas como um apoio nesse processo:",
    "Confira os pontos que podem ser ajustados para um desempenho mais completo:"
    ],
    'motivacao_regular': [
           "Com pequenos ajustes e foco contínuo, você poderá alcançar resultados ainda mais expressivos!",
    "Você possui um grande potencial — com determinação, é possível transformar pontos de atenção em fortalezas.",
    "Acredite no seu crescimento, pois cada passo na direção certa já representa um avanço significativo!",
    "Pequenas melhorias feitas com consistência têm o poder de gerar grandes transformações!",
    "Foco nos ajustes necessários e, com seu esforço, você irá superar as expectativas!",
    "Todo desafio é uma oportunidade disfarçada — enfrente-os com coragem e confiança.",
    "O caminho para a excelência é construído com resiliência, foco e dedicação diária.",
    "Você tem tudo para evoluir — basta direcionar seu esforço com estratégia e disciplina.",
    "Transformar pontos fracos em pontos fortes é uma habilidade que você pode desenvolver.",
    "A jornada de crescimento é feita de desafios — aceite-os como parte do seu sucesso."
    ],
    'alerta_critico': [
     "Recomendamos atenção especial a esses pontos, pois tratam-se de áreas críticas para seu desenvolvimento.",
    "Esses aspectos demandam sua prioridade para que o próximo ciclo seja mais produtivo e alinhado aos objetivos da equipe.",
    "Sugerimos foco imediato nesses pontos específicos para garantir um desempenho mais equilibrado.",
    "Essas questões precisam de ação imediata, mas estamos confiantes na sua capacidade de superá-las com apoio adequado.",
    "Priorize essas melhorias no próximo ciclo e conte conosco nesse processo de crescimento.",
    "É essencial tratar esses pontos com urgência e compromisso para evitar impactos futuros.",
    "Sua atuação precisa de ajustes imediatos nestes aspectos — estamos aqui para apoiar essa transição.",
    "Essas falhas não definem você, mas precisam ser enfrentadas com seriedade e responsabilidade.",
    "A superação destes desafios será determinante para sua continuidade e evolução na equipe.",
    "Reforçamos que mudanças consistentes nestas áreas são indispensáveis a partir do próximo ciclo."
    ],
    'frase_motivacional': [
    "Acredite no seu potencial e nunca subestime o poder de evoluir continuamente.",
    "Grandes conquistas começam com pequenos passos dados com coragem e consistência.",
    "O sucesso é a soma de pequenos esforços repetidos com determinação todos os dias.",
    "Você é capaz de ir além do que imagina — confie no seu talento e siga em frente!",
    "Cada novo dia é uma oportunidade única para aprender, crescer e brilhar ainda mais.",
    "Persistência, resiliência e foco são chaves para alcançar o êxito — continue com elas!",
    "Seu crescimento profissional está em suas mãos e cada decisão conta nesse caminho.",
    "Nada é impossível para quem acredita, planeja e age com propósito.",
    "O futuro pertence àqueles que acreditam na beleza de seus sonhos e agem para realizá-los.",
    "Sucesso não é ausência de falhas, mas sim a persistência mesmo diante delas."
    ],
    'despedida': [
    "Atenciosamente, Equipe de Gestão — seguimos juntos rumo à excelência!",
    "Com estima, Equipe de RH — estamos aqui para apoiar seu desenvolvimento.",
    "Cordiais saudações, Coordenação de Pessoas — conte conosco para crescer ainda mais.",
    "Com os melhores cumprimentos, Gestão de Talentos — seguimos juntos em busca do melhor.",
    "Respeitosamente, Equipe de Desenvolvimento — agradecemos por sua dedicação.",
    "Conte conosco no seu crescimento contínuo. Um forte abraço!",
    "Seguimos juntos em direção à excelência. Um cordial cumprimento!",
    "Obrigado por sua dedicação. Até o próximo ciclo!",
    "Estamos sempre ao seu lado nessa jornada. Grande abraço!",
    "Desejamos sucesso contínuo em seus próximos desafios!"
    ]
}

CLASSIFICACOES = {
    "Excelente": {
        "titulo": [
            "DESEMPENHO EXCEPCIONAL", 
            "RESULTADOS EXCELENTES",
            "PERFORMANCE DESTACADA",
            "NOTA MÁXIMA",
            "TOP PERFORMER"
        ],
        "frases": [
            "Seu trabalho tem sido exemplar!",
            "Continue assim!",
            "Você é uma referência para a equipe!",
            "Seu desempenho inspira os colegas!",
            "Mantenha esse brilho!"
        ]
    },
    "Muito Bom": {
        "titulo": [
            "ÓTIMO DESEMPENHO", 
            "RESULTADOS MUITO BONS",
            "ALTO NÍVEL",
            "PERFORMANCE ELEVADA",
            "DESTAQUE POSITIVO"
        ],
        "frases": [
            "Seu desempenho está acima da média!",
            "Ótimo trabalho!",
            "Você está entre os melhores!",
            "Quase perfeito!",
            "Falta pouco para a excelência!"
        ]
    },
    "Bom": {
        "titulo": [
            "BOM DESEMPENHO", 
            "RESULTADOS SATISFATÓRIOS",
            "NÍVEL ADEQUADO",
            "PERFORMANCE SOLIDÁRIA",
            "RESULTADOS POSITIVOS"
        ],
        "frases": [
            "Seu trabalho está bom, mas pode melhorar!",
            "Bom desempenho!",
            "Você está no caminho certo!",
            "Com ajustes, você chega mais longe!",
            "Bom trabalho, mas não pare por aqui!"
        ]
    },
    "Regular": {
        "titulo": [
            "DESEMPENHO REGULAR", 
            "RESULTADOS DENTRO DO ESPERADO",
            "NÍVEL BÁSICO",
            "PERFORMANCE MÉDIA",
            "RESULTADOS REGULARES"
        ],
        "frases": [
            "Há espaço para melhorias!",
            "Podemos melhorar juntos!",
            "Você pode dar mais de si!",
            "Acredite no seu potencial!",
            "Com esforço, você pode melhorar!"
        ]
    },
    "Crítico": {
        "titulo": [
            "DESEMPENHO ABAIXO DO ESPERADO", 
            "ATENÇÃO: NECESSÁRIO MELHORIAS",
            "ALERTA: PERFORMANCE BAIXA",
            "NECESSIDADE DE AJUSTES",
            "RESULTADOS INSATISFATÓRIOS"
        ],
        "frases": [
            "Precisamos conversar sobre seu desempenho.",
            "Situação que requer atenção.",
            "Seu desempenho está abaixo do esperado.",
            "Vamos trabalhar juntos para melhorar.",
            "Requer ação imediata para correção."
        ]
    }
}

DICAS_MELHORIA = {
    'Assiduidade': [
        "Dica: Mantenha a consistência em sua presença.",
        "Sugestão: Planeje sua agenda com antecedência para evitar faltas.",
        "Recomendação: Cuide da sua saúde física e mental para minimizar ausências.",
        "Orientações: Comunique ausências com antecedência ao responsável.",
        "Ação: Estabeleça uma rotina diária mais regular.",
        "Dica: Evite compromissos que possam interferir no horário de trabalho.",
        "Sugestão: Utilize alarmes ou lembretes para garantir sua presença.",
        "Recomendação: Avalie o impacto das faltas no seu desempenho e equipe.",
        "Orientações: Busque apoio se estiver enfrentando dificuldades pessoais.",
        "Ação: Registre e reflita sobre suas ausências para identificar padrões."
    ],
    'Pontualidade': [
        "Dica: Programe-se para chegar com 10 a 15 minutos de antecedência.",
        "Sugestão: Antecipe imprevistos no trajeto, como trânsito ou clima.",
        "Recomendação: Verifique o trânsito e transporte público antes de sair.",
        "Orientações: Ajuste seu relógio ou celular alguns minutos adiantado.",
        "Ação: Estabeleça uma meta pessoal de pontualidade diária.",
        "Dica: Prepare tudo o que precisa na noite anterior.",
        "Sugestão: Evite distrações pela manhã, como celular ou TV.",
        "Recomendação: Durma cedo para garantir disposição ao acordar.",
        "Orientações: Tenha um plano B para o transporte em caso de imprevistos.",
        "Ação: Use aplicativos de organização para otimizar seus horários."
    ],
    'Cumprimento de Tarefas': [
        "Dica: Priorize as atividades mais importantes e urgentes.",
        "Sugestão: Use listas de tarefas ou aplicativos de produtividade.",
        "Recomendação: Estime com realismo o tempo necessário para cada tarefa.",
        "Orientações: Peça ajuda ou orientação quando encontrar dificuldades.",
        "Ação: Foque em uma tarefa por vez para evitar retrabalho.",
        "Dica: Faça pequenas pausas para manter a produtividade.",
        "Sugestão: Estabeleça metas diárias ou semanais.",
        "Recomendação: Revise o que foi feito ao final do dia.",
        "Orientações: Divida tarefas grandes em etapas menores.",
        "Ação: Elimine distrações durante a execução das tarefas."
    ],
    'Comportamento': [
        "Dica: O diálogo é a chave para bons relacionamentos interpessoais.",
        "Sugestão: Pratique a escuta ativa com colegas e superiores.",
        "Recomendação: Mantenha postura profissional em todos os momentos.",
        "Orientações: Participe mais das atividades e reuniões em equipe.",
        "Ação: Desenvolva sua inteligência emocional para lidar com conflitos.",
        "Dica: Demonstre respeito pelas opiniões e diferenças dos outros.",
        "Sugestão: Evite fofocas e comentários negativos no ambiente de trabalho.",
        "Recomendação: Aprenda a receber feedbacks de forma construtiva.",
        "Orientações: Seja proativo e ofereça ajuda quando possível.",
        "Ação: Controle reações impulsivas e busque sempre a empatia."
    ]
}


def selecionar_frase(chave, **kwargs):
    """Seleciona uma frase aleatória do banco e aplica os parâmetros"""
    frase = random.choice(BANCO_FRASES[chave])
    return frase.format(**kwargs)

def gerar_titulo(classificacao):
    """Gera um título aleatório baseado na classificação"""
    return random.choice(CLASSIFICACOES[classificacao]["titulo"])

def selecionar_dica(categoria):
    """Seleciona uma dica aleatória para a categoria especificada"""
    return random.choice(DICAS_MELHORIA.get(categoria, ["Dica: Foco na melhoria contínua"]))

def analisar_desempenho(nota):
    """Determina a classificação baseado na nota"""
    try:
        nota = float(nota)
    except (ValueError, TypeError):
        return "Crítico"
    
    if nota >= 9: return "Excelente"
    elif nota >= 8: return "Muito Bom"
    elif nota >= 7: return "Bom"
    elif nota >= 5: return "Regular"
    else: return "Crítico"

def formatar_mes(mes):
    """Formata o número do mês para nome"""
    try:
        mes_num = int(mes)
        if 1 <= mes_num <= 12:
            meses = [
                "janeiro", "fevereiro", "março", "abril", "maio", "junho",
                "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
            ]
            return meses[mes_num - 1]
        return str(mes)
    except (ValueError, TypeError):
        return str(mes)  # Retorna o mês original se a conversão falhar

def gerar_feedback(nome, cargo, mes, assiduidade, pontualidade, cumprimento_tarefas, comportamento, nota_final):
    # Determinar classificação
    classificacao = analisar_desempenho(nota_final)
    
    # Formatar mês
    mes_extenso = formatar_mes(mes)
    
    # Iniciar construção do feedback
    feedback = []
    
    # Adicionar cabeçalho
    feedback.append("=" * 70)
    feedback.append(gerar_titulo(classificacao))
    feedback.append("=" * 70)
    feedback.append("")
    
    # Saudação personalizada
    feedback.append(selecionar_frase('saudacao', nome=nome))
    feedback.append("")
    
    # Introdução
    feedback.append(selecionar_frase('introducao', mes=mes_extenso))
    feedback.append("")
    
    # Feedback geral baseado na classificação
    if classificacao in ["Excelente", "Muito Bom"]:
        feedback.append(selecionar_frase('elogio_geral', classificacao=classificacao, nota=nota_final))
        feedback.append("")
        
        # Identificar pontos fortes (notas >= 7)
        pontos_fortes = []
        if assiduidade != '-' and float(assiduidade) >= 7:
            pontos_fortes.append(f"✔ Assiduidade: {assiduidade}/10")
        if pontualidade != '-' and float(pontualidade) >= 7:
            pontos_fortes.append(f"✔ Pontualidade: {pontualidade}/10")
        if cumprimento_tarefas != '-' and float(cumprimento_tarefas) >= 7:
            pontos_fortes.append(f"✔ Cumprimento de Tarefas: {cumprimento_tarefas}/10")
        if comportamento != '-' and float(comportamento) >= 7:
            pontos_fortes.append(f"✔ Comportamento: {comportamento}/10")
        
        if pontos_fortes:
            feedback.append(selecionar_frase('elogio_pontos_fortes'))
            feedback.extend(pontos_fortes)
            feedback.append("")
        
        feedback.append(selecionar_frase('encorajamento'))
    
    elif classificacao == "Bom":
        feedback.append(f"Seu desempenho foi {classificacao} (nota {nota_final}). {random.choice(CLASSIFICACOES[classificacao]['frases'])}")
        feedback.append("")
        
        # Pontos fortes
        pontos_fortes = []
        if assiduidade != '-' and float(assiduidade) >= 6:
            pontos_fortes.append(f"✓ Assiduidade: {assiduidade}/10")
        if pontualidade != '-' and float(pontualidade) >= 6:
            pontos_fortes.append(f"✓ Pontualidade: {pontualidade}/10")
        if cumprimento_tarefas != '-' and float(cumprimento_tarefas) >= 6:
            pontos_fortes.append(f"✓ Cumprimento de Tarefas: {cumprimento_tarefas}/10")
        if comportamento != '-' and float(comportamento) >= 6:
            pontos_fortes.append(f"✓ Comportamento: {comportamento}/10")
        
        if pontos_fortes:
            feedback.append("Seus destaques este mês:")
            feedback.extend(pontos_fortes)
            feedback.append("")
        
        # Áreas para melhoria (notas < 6)
        areas_melhoria = []
        if assiduidade != '-' and float(assiduidade) < 6:
            dica = selecionar_dica('Assiduidade')
            areas_melhoria.append(f"↗ Assiduidade: {assiduidade}/10 - {dica}")
        if pontualidade != '-' and float(pontualidade) < 6:
            dica = selecionar_dica('Pontualidade')
            areas_melhoria.append(f"↗ Pontualidade: {pontualidade}/10 - {dica}")
        if cumprimento_tarefas != '-' and float(cumprimento_tarefas) < 6:
            dica = selecionar_dica('Cumprimento de Tarefas')
            areas_melhoria.append(f"↗ Cumprimento de Tarefas: {cumprimento_tarefas}/10 - {dica}")
        if comportamento != '-' and float(comportamento) < 6:
            dica = selecionar_dica('Comportamento')
            areas_melhoria.append(f"↗ Comportamento: {comportamento}/10 - {dica}")
        
        if areas_melhoria:
            feedback.append(selecionar_frase('sugestao_melhoria'))
            feedback.extend(areas_melhoria)
        
        feedback.append("")
        feedback.append(selecionar_frase('motivacao_regular'))
    
    elif classificacao == "Regular":
        feedback.append(f"Seu desempenho foi {classificacao} (nota {nota_final}). {random.choice(CLASSIFICACOES[classificacao]['frases'])}")
        feedback.append("")
        
        # Pontos positivos (notas >= 5)
        pontos_positivos = []
        if assiduidade != '-' and float(assiduidade) >= 5:
            pontos_positivos.append(f"• Assiduidade: {assiduidade}/10")
        if pontualidade != '-' and float(pontualidade) >= 5:
            pontos_positivos.append(f"• Pontualidade: {pontualidade}/10")
        if cumprimento_tarefas != '-' and float(cumprimento_tarefas) >= 5:
            pontos_positivos.append(f"• Cumprimento de Tarefas: {cumprimento_tarefas}/10")
        if comportamento != '-' and float(comportamento) >= 5:
            pontos_positivos.append(f"• Comportamento: {comportamento}/10")
        
        if pontos_positivos:
            feedback.append("Alguns aspectos positivos:")
            feedback.extend(pontos_positivos)
            feedback.append("")
        
        # Áreas críticas (notas < 5)
        areas_criticas = []
        if assiduidade != '-' and float(assiduidade) < 5:
            dica = selecionar_dica('Assiduidade')
            areas_criticas.append(f"⚠ Assiduidade: {assiduidade}/10 - {dica}")
        if pontualidade != '-' and float(pontualidade) < 5:
            dica = selecionar_dica('Pontualidade')
            areas_criticas.append(f"⚠ Pontualidade: {pontualidade}/10 - {dica}")
        if cumprimento_tarefas != '-' and float(cumprimento_tarefas) < 5:
            dica = selecionar_dica('Cumprimento de Tarefas')
            areas_criticas.append(f"⚠ Cumprimento de Tarefas: {cumprimento_tarefas}/10 - {dica}")
        if comportamento != '-' and float(comportamento) < 5:
            dica = selecionar_dica('Comportamento')
            areas_criticas.append(f"⚠ Comportamento: {comportamento}/10 - {dica}")
        
        if areas_criticas:
            feedback.append("Áreas que precisam de atenção imediata:")
            feedback.extend(areas_criticas)
            feedback.append("")
        
        feedback.append(selecionar_frase('alerta_critico'))
    
    else:  # Crítico
        feedback.append(f"Seu desempenho foi classificado como {classificacao} (nota {nota_final}). {random.choice(CLASSIFICACOES[classificacao]['frases'])}")
        feedback.append("")
        
        feedback.append("Identificamos pontos críticos que exigem ação imediata:")
        
        areas_criticas = []
        if assiduidade != '-' and float(assiduidade) < 5:
            dica = selecionar_dica('Assiduidade')
            areas_criticas.append(f"❌ Assiduidade: {assiduidade}/10 - {dica}")
        if pontualidade != '-' and float(pontualidade) < 5:
            dica = selecionar_dica('Pontualidade')
            areas_criticas.append(f"❌ Pontualidade: {pontualidade}/10 - {dica}")
        if cumprimento_tarefas != '-' and float(cumprimento_tarefas) < 5:
            dica = selecionar_dica('Cumprimento de Tarefas')
            areas_criticas.append(f"❌ Cumprimento de Tarefas: {cumprimento_tarefas}/10 - {dica}")
        if comportamento != '-' and float(comportamento) < 5:
            dica = selecionar_dica('Comportamento')
            areas_criticas.append(f"❌ Comportamento: {comportamento}/10 - {dica}")
        
        feedback.extend(areas_criticas)
        feedback.append("")
        feedback.append("Vamos agendar uma conversa o mais breve possível para traçarmos um plano de ação conjunto.")
    
    # Frase motivacional final
    feedback.append("")
    feedback.append(selecionar_frase('frase_motivacional'))
    feedback.append("")
    
    # Despedida
    feedback.append(selecionar_frase('despedida'))
    
    return "\n".join(feedback)

def processar_csv(nome_arquivo):
    try:
        with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            
            for linha in leitor:
                # Tratar valores ausentes
                assiduidade = linha.get('Assiduidade', '-')
                pontualidade = linha.get('Pontualidade', '-')
                cumprimento_tarefas = linha.get('Cumprimento Tarefas', '-')
                comportamento = linha.get('Comportamento', '-')
                
                feedback = gerar_feedback(
                    nome=linha.get('Nome', ''),
                    cargo=linha.get('Cargo', ''),
                    mes=linha.get('Mês', ''),
                    assiduidade=assiduidade,
                    pontualidade=pontualidade,
                    cumprimento_tarefas=cumprimento_tarefas,
                    comportamento=comportamento,
                    nota_final=linha.get('Nota Final', '0')
                )
                
                print(feedback)
                #print("\n" + "="*70 + "\n")
                mensagem_final = " ".join(feedback).replace("  ", " ")
                return {"data": mensagem_final}
                
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {str(e)}")
        
def gerar_feedback_individual(codigo_funcionario):
    """Gera feedback para um único funcionário baseado no código/ID"""
    nome_arquivo = 'static/dados_funcionarios.csv'
    try:
        with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            funcionario_encontrado = False

            for linha in leitor:
                if linha.get('Codigo', '').strip() == str(codigo_funcionario).strip():
                    funcionario_encontrado = True

                    # Tratar valores ausentes
                    assiduidade = linha.get('Assiduidade', '-')
                    pontualidade = linha.get('Pontualidade', '-')
                    cumprimento_tarefas = linha.get('Cumprimento Tarefas', '-')
                    comportamento = linha.get('Comportamento', '-')
                    nota_final = linha.get('Nota Final', '0')

                    feedback = gerar_feedback(
                        nome=linha.get('Nome', ''),
                        cargo=linha.get('Cargo', ''),
                        mes=linha.get('Mes', ''),
                        assiduidade=assiduidade,
                        pontualidade=pontualidade,
                        cumprimento_tarefas=cumprimento_tarefas,
                        comportamento=comportamento,
                        nota_final=nota_final
                    )

                    print(f"Feedback para o funcionário {linha.get('Nome', '')} (Código: {codigo_funcionario}):\n")
                    print(feedback)

                    return {"data": feedback, "message": "Feedback gerado com sucesso", "status": "success"}

            if not funcionario_encontrado:
                print(f"Funcionário com código {codigo_funcionario} não encontrado.")
                return {"data": "", "message": "Funcionário não encontrado", "status": "error"}

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return {"data": "", "message": f"Arquivo '{nome_arquivo}' não encontrado", "status": "error"}
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {str(e)}")
        return {"data": "", "message": str(e), "status": "error"}
    
def gerar_feedback_por_dados(dados_funcionario):
    """Gera feedback a partir de um dicionário com os dados do funcionário"""
    try:
        # Extrair e tratar os dados recebidos
        nome = dados_funcionario.get('Nome', 'Funcionário')
        cargo = dados_funcionario.get('Cargo', 'Não informado')
        mes = dados_funcionario.get('Mes', '-')
        assiduidade = dados_funcionario.get('Assiduidade', '-')
        pontualidade = dados_funcionario.get('Pontualidade', '-')
        cumprimento_tarefas = dados_funcionario.get('Cumprimento Tarefas', '-')
        comportamento = dados_funcionario.get('Comportamento', '-')
        nota_final = dados_funcionario.get('Nota Final', '0')

        # Gerar o texto do feedback usando função já existente
        feedback = gerar_feedback(
            nome=nome,
            cargo=cargo,
            mes=mes,
            assiduidade=assiduidade,
            pontualidade=pontualidade,
            cumprimento_tarefas=cumprimento_tarefas,
            comportamento=comportamento,
            nota_final=nota_final
        )

        print(f"Feedback para o funcionário {nome} (Código: {dados_funcionario.get('Codigo', 'N/A')}):\n")
        print(feedback)

        return {
            "data": feedback,
            "message": "Feedback gerado com sucesso",
            "status": "success"
        }

    except Exception as e:
        print(f"Erro ao gerar feedback: {str(e)}")
        return {
            "data": "",
            "message": f"Erro ao gerar feedback: {str(e)}",
            "status": "error"
        }


def menu_principal():
    while True:
        print("\nSistema de Feedback de Funcionários")
        print("1. Gerar feedbacks para todos os funcionários")
        print("2. Gerar feedback para um funcionário específico")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            processar_csv('static/dados_funcionarios.csv')
        elif opcao == "2":
            codigo = input("Digite o código do funcionário: ")
            gerar_feedback_individual(codigo)
        elif opcao == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        input("\nPressione Enter para continuar...")

# Iniciar o sistema
if __name__ == "__main__":
    menu_principal()
    