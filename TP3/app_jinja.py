import requests
from flask_cors import CORS
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'História de Portugal'
CORS(app)

# Initialize score
@app.before_request
def initialize_session():
    if 'score' not in session:
        session['score'] = 0

# Web Routes
@app.route('/')
def home():
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question_text = request.form.get('question')

        # Enviar a resposta do user para a API
        response = requests.post('http://localhost:5001/api/answer', json={'question': question_text, 'answer': user_answer, 'score': session['score']})

        if response.status_code == 200:
            data = response.json()
            session['score'] = data['score']
            return render_template('result.html', correct=data['correct'], correct_answer=data['correct_answer'], score=data['score'], user_answer=user_answer, question = question_text)
        else:
            return render_template('error.html', message="Erro ao validar a resposta.")

    elif request.method == 'GET':
        # Buscar uma nova pergunta na API
        response = requests.get('http://localhost:5001/api/quiz')

        if response.status_code == 200:
            question = response.json()
            return render_template('quiz.html', question=question)
        else:
            return render_template('error.html', message="Erro ao buscar pergunta.")

    return render_template('error.html', message="Método não suportado.")


@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)
