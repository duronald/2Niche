from flask import Flask, render_template, session
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'mysecretkey'
Session(app)

@app.route('/')
def home():
    session['username'] = 'John'
    return render_template('home.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)