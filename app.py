import os

from flask import Flask, render_template, request, make_response, send_from_directory
import xml.etree.ElementTree as ET
app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/about')
def about():
    return render_template('about.html')
# comment

@app.route('/task1')
def task1():
    return render_template('task1.html')


@app.route('/task2')
def task2():
    return render_template('task2.html')


# Функция для парсинга XML файла


@app.route('/show_server_config', methods=['GET', 'POST'])
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
def task3():
    return render_template('task3.html')

@app.route('/task4')
def task4():
    return render_template('task4.html')

@app.route('/ctf')
def ctf():
    return render_template('ctf.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/logi')
def logi():
    return render_template('logi.html')

@app.route('/head', methods=['GET', 'HEAD'])
def test_head():
    if request.method == 'GET':
        return "Головой подумой!"
    response = make_response()
    response.headers['FLAG'] = 'mgnh1lls{1_h4v3_4_h34d4ch3}'
    return response


@app.route('/check_header')
def check_header():
    required_header = 'PILL'

    if request.headers.get(required_header) == 'PARACETAMOL':
        return "mgnh1lls{1_d0n7_h4v3_4_h34d4ch3}"
    else:
        return "I have a headache give me a PILL of PARACETAMOL"


@app.route('/files/chat.exe')
def download_file():
    file_name = 'zaglushka.txt'
    return send_from_directory('files', file_name, as_attachment=True)


if __name__ == ('__main__'):
    app.run(debug=True)