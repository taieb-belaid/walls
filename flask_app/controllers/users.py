from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.message import Message

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('registration_login.html')

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/walls')
def walls():
    data = {
        'id' : session['user_id']
    }
    return render_template('walls.html',user = User.get_user_by_id(data), list_of_users = User.get_all_users(data),messages = Message.show_messages(data) )


@app.route('/sign_up',methods=['POST'])
def sign_up():
    if User.valid_registration(request.form):
        User.save(request.form)
        flash('Registration succed')
        return redirect('/')
    return redirect('/')    

@app.route('/sign_in',methods=['POST'])
def sign_in():
    user = User.get_user_by_mail(request.form)
    if not user:
        flash('email or password incorrect')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password ,request.form['password']):
        flash('email or password incorrect')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/walls')
