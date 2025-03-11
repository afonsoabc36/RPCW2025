import random
import requests
from flask_cors import CORS
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'Historia de Portugal'
CORS(app)

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/HistoriaPT"
prefixes = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
"""

cognomes_query = prefixes + """
    SELECT ?o WHERE {
    ?su a :Rei ;
	   :cognomes ?o.
    }
"""
dinastias_query = prefixes + """
SELECT DISTINCT ?o WHERE {
     ?di a :Dinastia;
    		:nome ?o.
    }
"""
partidos_query = prefixes + """
SELECT ?s ?o WHERE {
    ?si a :Partido ;
        :nome ?o;
}
"""

cognomes = requests.get(GRAPHDB_ENDPOINT, params={'query': cognomes_query}, headers={'Accept': 'application/json'}).json()['results']['bindings']
cognomes_list = [cognome['o']['value'] for cognome in cognomes]

dinastias = requests.get(GRAPHDB_ENDPOINT, params={'query': dinastias_query}, headers={'Accept': 'application/json'}).json()['results']['bindings']
dinastias_list = [dinastia['o']['value'] for dinastia in dinastias]

partidos = requests.get(GRAPHDB_ENDPOINT, params={'query': partidos_query}, headers={'Accept': 'application/json'}).json()['results']['bindings']
partidos_list = [partido['o']['value'] for partido in partidos]

# Lista de perguntas dinâmicas
question_queries = {
    "nascimento": (prefixes + """
    SELECT ?s ?o WHERE {
        ?r a :Rei;
           :nome ?s;
           :nascimento ?o.
    }
    """, "Em que ano nasceu o Rei {subject}?", "multiple_choice"),
    "cognomes": (prefixes + """
    SELECT ?s ?o WHERE {
    ?su a :Rei ;
	   :nome ?s;
       :nascimento ?d;
	   :cognomes ?o.
    }
    """, "O Rei {subject} tem o cognome {obj}.", "true_false"),
    "descobrimentos": (prefixes + """
    SELECT ?s ?o WHERE {
        ?de a :Descobrimento;
           :temReinado ?r;
    		:notas ?s.
    	?r :dinastia ?di.
    	?di :nome ?o.
    }    """, "O descobrimento descrito por '{subject}' ocorreu durante a {obj}.", "true_false"),
    "nascimentoPresidente": (prefixes + """
    SELECT ?s ?o WHERE {
        ?si a :Presidente;
            :nome ?s;
            :nascimento ?o;
    }
    """, "O Presidente {subject} nasceu em que ano?", "multiple_choice"), 
    "mandatosPresidentes": (prefixes + """
    SELECT ?s (COUNT(?m) as ?o) WHERE {
        ?si a :Presidente;
            :nome ?s;
            :mandato ?m.
    }
    GROUP BY ?s
    """, "Quantos mandatos cumpriu o Presidente {subject}?", "multiple_choice"),
    "partidosMilitantes": (prefixes + """
     SELECT ?s ?o WHERE {
        ?si a :Partido ;
            :nome ?o;
           :temMilitante ?m.
        ?m :nome ?s.
    }""", "O Militante {subject} representa o partido {obj}.", "true_false")
}

# Função para buscar perguntas do GraphDB
def fetch_questions():
    headers = {'Accept': 'application/json'}
    questions = []

    for id, (sparql_query, question_text, question_type) in question_queries.items():
        response = requests.get(GRAPHDB_ENDPOINT, params={'query': sparql_query}, headers=headers)

        if response.status_code != 200:
            print(f"Erro ao buscar dados: {response.status_code}")
            continue

        data = response.json()

        for r in data['results']['bindings']:
            subject = r['s']['value']
            obj = r['o']['value']

            # Formata a pergunta com o nome do rei
            formatted_question = question_text.format(subject=subject, obj=obj)

            # Gera opções de resposta para múltipla escolha
            if question_type == "multiple_choice":
                if id == "nascimento" or id == "nascimentoPresidente":
                    obj = obj.split(" ")[-1]
                    correct_answer = int(obj)
                    incorrect_answers = set()
                    while len(incorrect_answers) < 3:
                        variation = random.randint(-10, 10)
                        fake_answer = correct_answer + variation
                        if fake_answer != correct_answer:
                            incorrect_answers.add(str(fake_answer))
                    # Criar a lista de opções e embaralhar
                    options = [str(correct_answer)] + list(incorrect_answers)
                    random.shuffle(options)
                elif id == "mandatosPresidentes":
                    options = ["1","2","3","4"]
                else:
                    options = []
            elif question_type == "true_false":
                if id == "cognomes":
                    if random.randint(1, 2) == 1:
                        otherCognome = obj
                        while otherCognome == obj:
                            otherCognome = random.choice(cognomes_list)
                        formatted_question = question_text.format(subject=subject, obj=otherCognome)
                        obj = "Falso"
                    else:
                        obj = "Verdadeiro"
                elif id == "descobrimentos":
                    if random.randint(1, 2) == 1:
                        otherDinastia = obj
                        while otherDinastia == obj:
                            otherDinastia = random.choice(dinastias_list)
                        formatted_question = question_text.format(subject=subject, obj=otherDinastia)
                        obj = "Falso"
                    else:
                        obj = "Verdadeiro"
                elif id == "partidosMilitantes":
                    if random.randint(1, 2) == 1:
                        otherPartido = obj
                        while otherPartido == obj:
                            otherPartido = random.choice(partidos_list)
                        formatted_question = question_text.format(subject=subject, obj=otherPartido)
                        obj = "Falso"
                    else:
                        obj = "Verdadeiro"
                options = ["Verdadeiro", "Falso"]
            else:
                options = []  # Caso precise adicionar outros tipos depois

            # Adiciona a pergunta formatada
            questions.append({
                "question": formatted_question,
                "options": options,
                "answer": obj,
                "type": question_type
            })
    
    return questions

# Load questions from GraphDB
questions = fetch_questions()

@app.route('/api/quiz', methods=['GET'])
def get_question():
    if not questions:
        return jsonify({'error': 'No questions available'}), 500
    
    question = random.choice(questions)
    return jsonify({
        'question': question['question'],
        'options': question['options'],
        'type': question['type']
    })

@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.json or {}
    user_answer = data.get('answer')
    question_text = data.get('question')
    session['score'] = data.get('score')
    
    for question in questions:
        if question['question'] == question_text:
            correct = question['answer'] == user_answer
            session['score'] = session.get('score', 0) + (1 if correct else 0)
            return jsonify({
                'correct': correct,
                'correct_answer': question['answer'],
                'score': session['score']
            })
    
    return jsonify({'error': 'Question not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
