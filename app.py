from flask import Flask, render_template

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


if __name__ == ('__main__'):
    app.run(debug=True)