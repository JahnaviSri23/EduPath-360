# app.py
from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)
app.secret_key = "edupath_secret"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'janu@#.200723'
app.config['MYSQL_DB'] = 'edupath360'

mysql = MySQL(app)

# Upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ===== Utils for quiz =====
quiz_questions = [
    {
        "question": "Do you enjoy solving math problems?",
        "options": ["Yes", "No", "Sometimes"]
    },
    {
        "question": "Do you like creative arts?",
        "options": ["Yes", "No", "Sometimes"]
    },
    {
        "question": "Do you enjoy working with computers?",
        "options": ["Yes", "No", "Sometimes"]
    },
]

career_paths = {
    "Science": ["Engineering", "Medicine", "Research Scientist"],
    "Arts": ["Design", "Literature", "Performing Arts"],
    "Commerce": ["CA", "Business Management", "Economics"]
}

districts_list = ["Hyderabad", "Warangal", "Karimnagar"]  # Example districts
colleges_data = {
    "Hyderabad": [
        {"name": "Govt College A", "seats": 120, "entrance_exam": "EAMCET", "exam_date": "2026-06-01"},
        {"name": "Govt College B", "seats": 100, "entrance_exam": "NEET", "exam_date": "2026-06-10"},
    ],
    "Warangal": [
        {"name": "Govt College C", "seats": 80, "entrance_exam": "EAMCET", "exam_date": "2026-06-05"},
    ],
    "Karimnagar": [
        {"name": "Govt College D", "seats": 90, "entrance_exam": "NEET", "exam_date": "2026-06-08"},
    ]
}

# ===== Routes =====

@app.route('/')
def home():
    return render_template('login.html')

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        class_completed = request.form['class_completed']

        # Upload mark list
        file = request.files['marklist']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, mobile, class_completed, marklist) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (name, email, password, mobile, class_completed, filename)
        )
        mysql.connection.commit()
        cursor.close()
        return redirect('/')
    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['loggedin'] = True
        session['user_id'] = user['id']
        session['name'] = user['name']
        return redirect('/dashboard')
    else:
        return "Invalid Email or Password"

# ---------- DASHBOARD ----------
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', name=session['name'])
    return redirect('/')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------- SELECT EXAM ----------
@app.route('/select_exam')
def select_exam():
    if 'loggedin' not in session:
        return redirect('/')
    return render_template('select_exam.html')

# ---------- EXAM ----------
@app.route('/exam')
def exam():
    if 'loggedin' not in session:
        return redirect('/')
    exam_type = request.args.get('type', 'aptitude')
    return render_template('exam.html', exam_type=exam_type, questions=quiz_questions)

# ---------- SUBMIT EXAM ----------
@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    if 'loggedin' not in session:
        return redirect('/')

    score_science = 0
    score_arts = 0
    score_commerce = 0

    for i, q in enumerate(quiz_questions):
        answer = request.form.get(f'q{i}')
        if i == 0 and answer == "Yes":
            score_science += 1
        elif i == 1 and answer == "Yes":
            score_arts += 1
        elif i == 2 and answer == "Yes":
            score_commerce += 1

    # Determine career path
    max_score = max(score_science, score_arts, score_commerce)
    if max_score == score_science:
        path = career_paths["Science"]
    elif max_score == score_arts:
        path = career_paths["Arts"]
    else:
        path = career_paths["Commerce"]

    career_suggestion = ", ".join(path)
    return render_template('result.html', career_path=career_suggestion)

# ---------- SELECT DISTRICT ----------
@app.route('/select_district', methods=['GET', 'POST'])
def select_district():
    if 'loggedin' not in session:
        return redirect('/')
    return render_template('select_district.html', districts=districts_list)

# ---------- DISPLAY COLLEGES ----------
@app.route('/college_list', methods=['POST'])
def college_list():
    if 'loggedin' not in session:
        return redirect('/')
    district = request.form['district']
    colleges = colleges_data.get(district, [])
    return render_template('college_list.html', district=district, colleges=colleges)

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)