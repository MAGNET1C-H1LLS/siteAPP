from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/task1')
def task1():
    return render_template('task1.html')


@app.route('/task2')
def task2():
    return render_template('task2.html')

@app.route('/show_server_config', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_option = request.form['option']
        if selected_option == '1':
            text = 'hello'
        elif selected_option == '2':
            text = 'bye-bye'
        else:
            text = ''
        return render_template('task2.html', text=text)
    return render_template('task2.html', text='')


@app.route('/task3')
def task3():
    return render_template('task3.html')


@app.route('/task4')
def task4():
    return render_template('task4.html')


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
    


if __name__ == ('__main__'):
    app.run(debug=True)