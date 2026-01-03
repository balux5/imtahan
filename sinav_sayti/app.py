from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'secret_key'

with open('questions_1.json', 'r', encoding='utf-8') as f:
    questions_1 = json.load(f)
with open('questions_2.json', 'r', encoding='utf-8') as f:
    questions_2 = json.load(f)
with open('questions_3.json', 'r', encoding='utf-8') as f:
    questions_3 = json.load(f)
with open('questions_4.json', 'r', encoding='utf-8') as f:
    questions_4 = json.load(f)
with open('questions_5.json', 'r', encoding='utf-8') as f:
    questions_5 = json.load(f)
with open('questions_6.json', 'r', encoding='utf-8') as f:
    questions_6 = json.load(f)
with open('questions_7.json', 'r', encoding='utf-8') as f:
    questions_7 = json.load(f)
with open('questions_8.json', 'r', encoding='utf-8') as f:
    questions_8 = json.load(f)

users_attempted = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        class_grade = request.form['class_grade']
        if users_attempted.get(username):
            return "Siz artiq sinava girdiniz!"
        session['username'] = username
        session['class_grade'] = class_grade
        session['start_time'] = datetime.now().isoformat()
        return redirect(url_for('exam'))
    return render_template('login.html')

@app.route('/exam', methods=['GET', 'POST'])
def exam():
    if 'username' not in session:
        return redirect(url_for('login'))

    start_time = datetime.fromisoformat(session['start_time'])
    end_time = start_time + timedelta(hours=2)
    if datetime.now() > end_time:
        users_attempted[session['username']] = True
        return "Vaxt bitdi!"

    grade = session['class_grade']
    if grade == "1":
        questions = questions_1
    elif grade == "2":
        questions = questions_2
    elif grade == "3":
        questions = questions_3
    elif grade == "4":
        questions = questions_4
    elif grade == "5":
        questions = questions_5
    elif grade == "6":
        questions = questions_6
    elif grade == "7":
        questions = questions_7
    elif grade == "8":
        questions = questions_8
    else:
        questions = []

    if request.method == 'POST':
        correct = 0
        wrong = 0
        for i, q in enumerate(questions, start=1):
            ans = request.form.get(f"q{i}")
            if ans == q['answer']:
                correct += 1
            else:
                wrong += 1
        users_attempted[session['username']] = True
        return f"Duz cavablar: {correct}, Sehv cavablar: {wrong}"

    return render_template('exam.html', questions=questions, end_time=end_time)

if __name__ == '__main__':
    app.run(debug=True)
