from flask import Flask, session, render_template, redirect, url_for


app = Flask(__name__)  

@app.route('/')
def home():
    if 'usr' in session:
        return render_template('dashboard.html',
                               user=session['usr'])
    else:
        return redirect(url_for('login'))
    
    
@app.route('/login')
def login():
    return render_template('login.html')