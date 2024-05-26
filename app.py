import os

from flask import Flask, render_template, request, make_response, send_from_directory, redirect, url_for, flash, send_file
import xml.etree.ElementTree as ET
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
from pprint import pprint


app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'logi'
context = ('./../certificate.crt', './../private.key')

forbidden_characters = (
    "--", "=", "<", ">", "!", '(', ')', "/*", "*/",
    ";", "'", '"', "\\", "%", "*", " ", "- -", 
    "UNION", "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "EXEC", "FROM",
    "CONCAT", "SUBSTRING",
    "AND", "OR", "NOT", "WHERE", "ORDER BY", "GROUP BY"
)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    with psycopg2.connect(DATABASE) as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM Users WHERE id = %s"
        cursor.execute(query, (int(user_id),))
        user = cursor.fetchone()
        if user:
            return User(id=user[0], username=user[1], password=user[2])
    return None

DATABASE = "postgresql://test:123@localhost:5432/test"

@app.before_request
def before_request():
    if not request.is_secure:
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/about')
def about():
    return render_template('about.html')
# comment

@app.route('/my_account')
@login_required
def my_account():
    sum_points = 0

    with psycopg2.connect(DATABASE) as con:
        with con.cursor() as curs:
            curs.execute(
                '''
                SELECT SUM(t.Point) AS total_points
                FROM done_tasks dt
                JOIN tasks t ON dt.task_id = t.id
                WHERE dt.user_id = %s;
                ''', (current_user.id, )
            )
            try:
                sum_points = int(curs.fetchone()[0])
            except:
                ...

            curs.execute('''
                SELECT u.name, COALESCE(SUM(t.point), 0) AS total_points
                FROM users u
                LEFT JOIN done_tasks dt ON u.id = dt.user_id
                LEFT JOIN tasks t ON dt.task_id = t.id
                GROUP BY u.name
                ORDER BY total_points DESC;
                ''')
            statistics = [(x[0], x[1]) for x in curs.fetchall()]
    return render_template('my_account.html',
                           username=current_user.username,
                           sum_points=sum_points,
                           statistics=statistics)

@app.route('/ctf')
@login_required
def ctf():
    ctf_tasks = []
    with psycopg2.connect(DATABASE) as con:
        with con.cursor() as curs:
            curs.execute('SELECT task_id FROM done_tasks WHERE user_id=%s', (current_user.id,))
            solved_tasks = [x[0] for x in curs.fetchall()]
            print(solved_tasks)

            curs.execute('SELECT * FROM categories;')

            for category in curs.fetchall():
                ctf_tasks.append(
                    {
                        'name': category[1],
                        'tasks': []
                    }
                )

                curs.execute('''
                    SELECT *
                    FROM tasks
                    WHERE category=%s
                    ORDER BY 
                        CASE difficult
                            WHEN 'easy' THEN 1
                            WHEN 'medium' THEN 2
                            WHEN 'medium-hard' THEN 3
                            WHEN 'hard' THEN 4
                            ELSE 5
                        END;
                ''', (category[0], ))

                for task in curs.fetchall():
                    ctf_tasks[-1]['tasks'].append(
                        {
                            'name': task[1], 
                            'difficulty': task[5],
                            'description': task[2],
                            'solved': 'True' if task[0] in solved_tasks else 'False'
                        }
                    )

    pprint(ctf_tasks)

    return render_template('ctf.html', categories=ctf_tasks)


@app.route('/h34dl355_h0r53m4n')
@login_required
def web2():
    if request.method == 'GET':
        return render_template('h34dl355_h0r53m4n.html')
    response = make_response()
    response.headers['FLAG'] = 'mgnh1lls{1_h4v3_4_h34d4ch3}'
    return response

@app.route('/h34ad4ch3')
@login_required
def web3():
    required_header = 'PILL'

    if request.headers.get(required_header) == 'PARACETAMOL':
        return "mgnh1lls{1_d0n7_h4v3_4_h34d4ch3}"
    else:
        return render_template('h34d4ch3.html')


@app.route('/task1')
@login_required
def task1():
    return render_template('task1.html')


@app.route('/task2')
@login_required
def task2():
    return render_template('task2.html')


# Функция для парсинга XML файла


@app.route('/show_server_config', methods=['GET', 'POST'])
@login_required
def show_server_config():
    if request.method == 'POST':
        selected_option = request.form['option']
        if selected_option == 'in':
            tree = ET.parse('static/text/in.xml')
        elif selected_option == 'out':
            tree = ET.parse('static/text/out.xml')


        root = tree.getroot()
        elements = [child.tag + ': ' + child.text for child in root]

        return render_template('task2.html', elements=elements)
    return render_template('task2.html', elements='')

@app.route('/task3')
@login_required
def task3():
    return render_template('task3.html')

@app.route('/task4')
@login_required
def task4():
    return render_template('task4.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
       username = filter_str(request.form['username'])
       password = filter_str(request.form['password'])
       confirm_password = filter_str(request.form['confirm_password'])
       print(username, password, confirm_password, sep='\n')

       if password != confirm_password:
           flash('Passwords do not match!', 'danger')
           return redirect(url_for('signup'))

       with psycopg2.connect(DATABASE) as connection:
           cursor = connection.cursor()
           query = "SELECT * FROM Users WHERE Name = %s"
           cursor.execute(query, (username,))
           user = cursor.fetchone()
           if user:
               flash('User already exists!', 'danger')
               return redirect(url_for('signup'))
           else:
               cursor.execute("INSERT INTO Users (Name, Password) VALUES (%s, %s)", (username, password))
               connection.commit()
               return redirect(url_for('logi'))
   else:
       return render_template("signup.html")



@app.route('/logi', methods=['GET', 'POST'])
def logi():
    if request.method == 'POST':
        username = filter_str(request.form['username'])
        password = filter_str(request.form['password'])
        print(username, password, sep=' ')
        with psycopg2.connect(DATABASE) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Users WHERE Name = %s AND Password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                user_obj = User(id=user[0], username=user[1], password=user[2])
                login_user(user_obj)
                print(user[0], user[1], user[2])
                return redirect(url_for('main_page'))
            else:
                print("ya check delay delay")
                flash("ВЫ КОНЧЕННЫЙ УРОДЕЦ", 'danger')
    return render_template("logi.html")

def filter_str(string: str) -> str:
    global forbidden_characters

    for substring in forbidden_characters:
        string = string.replace(substring, '').replace(substring.lower(), '')

    return string

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))

@app.route('/submit-task', methods=['POST'])
@login_required
def submit_task():
    if request.method == 'POST':
        answer = filter_str(request.form['answer'])
        task_title = request.form['popup_title']
        user_id = current_user.id

        with psycopg2.connect(DATABASE) as con:
            with con.cursor() as curs:
                print('CON')
                curs.execute('SELECT id FROM tasks WHERE name=%s AND flag=%s', (task_title, answer))
                print(answer)
                print('IM CHECK')
                task_id = curs.fetchone()
                if not task_id:
                    return ' '
                print('CHECK OK')

                curs.execute('''
                SELECT dt.user_id, t.Name, t.Point AS total_points
                FROM done_tasks dt
                JOIN tasks t ON dt.task_id = t.id
                WHERE dt.user_id = %s AND t.Name = %s;
                ''', (user_id, task_title))
                
                if curs.fetchone():
                    return ' '

                curs.execute('INSERT INTO done_tasks (task_id, user_id) VALUES (%s, %s)',
                             (task_id, user_id))
                con.commit()
                print('IM INSERT')
    return redirect(url_for('ctf'))

@app.route('/head', methods=['GET', 'HEAD'])
@login_required
def test_head():
    if request.method == 'GET':
        return "Головой подумой!"
    response = make_response()
    response.headers['FLAG'] = 'mgnh1lls{1_h4v3_4_h34d4ch3}'
    return response


@app.route('/check_header')
@login_required
def check_header():
    required_header = 'PILL'

    if request.headers.get(required_header) == 'PARACETAMOL':
        return "mgnh1lls{1_d0n7_h4v3_4_h34d4ch3}"
    else:
        return "I have a headache give me a PILL of PARACETAMOL"


@app.route('/files/chat.exe')
@login_required
def download_file():
    file_name = 'Chat.exe'
    return send_from_directory('files', file_name, as_attachment=True)

@app.route('/ctffiles/<filename>')
@login_required
def download_ctf_file(filename):
    download_dir = './ctffiles/'
    if '.zip' not in filename:  return 'НЕТ'
    if '/' in filename: return 'НЕЛЬЗЯ ТАК ДЕЛАТЬ'
    filepath = os.path.join(download_dir,filename)
    if os.path.isfile(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return 'Файл не найден'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443, ssl_context=context)
