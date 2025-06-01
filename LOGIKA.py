from flask import *
import sqlite3

app = Flask(__name__)


def init_and_show():
    conn = sqlite3.connect('BAZA2.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS LOGIN(
            id INTEGER PRIMARY KEY,
            login VARCHAR,
            password VARCHAR,
            avatar_url VARCHAR);
    ''')
    conn.commit()
    conn.close()
init_and_show()


@app.route('/')
def index():
    return render_template('mainsite.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    if username == '' or password == '':
        return "Пожалуйста введите логин и пароль"

    if len(username) < 3 or len(password) < 3:
        return "Логин и пароль должны быть больше 2 символов, а то непалучтя"

    conn = sqlite3.connect('BAZA2.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM LOGIN WHERE login = ? AND password = ?",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()

    if user:
        return render_template('profile.html')
    else:
        return "Неправильные данные"



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    password_confirm = request.form['password_confirm']

    if username == '' or password == '' or password_confirm == '':
        return "Пожалуйста заполните все"

    if len(username) < 3 or len(password) < 3:
        return "Логин и пароль должны быть больше 2 символов, а то не будешь регаться"

    if password != password_confirm:
        return "Пароли не совпадают, пожтому ещё раз."

    conn = sqlite3.connect('BAZA2.db')
    cur = conn.cursor()

    cur.execute("SELECT id FROM LOGIN WHERE login = ?", (username,))
    if cur.fetchone():
        conn.close()
        return "Пользователь с таким логином уже есть"

    cur.execute("INSERT INTO LOGIN (login, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return redirect('/login')


@app.route('/logout', methods=['POST'])
def logout():
    return render_template('login.html')


@app.route('/home', methods=['POST'])
def home():
    return render_template('mainsite.html')




@app.route('/SEX', methods=['GET', 'POST'])
def sex():
    print(1)


app.run(debug=False)