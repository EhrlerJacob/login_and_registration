from flask import render_template, redirect, session, request, flash 
from flask_app import app, bcrypt
from flask_app.models.user import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():

    if not User.validate_registration(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'], 
        "password": hashed_pw
    }
    one_user_id = User.save(data)
    session['logged_in_id'] = one_user_id
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    one_user = User.validate_login(request.form)
    if not one_user:
        return redirect('/')   
    session['logged_in_id'] = one_user.id
    return redirect ('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'logged_in_id' not in session:
        return redirect('/')
    data = {
        'id': session['logged_in_id']
    }
    return render_template('/dashboard.html', one_user= User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')