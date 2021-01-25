# encoding: utf-8

"""
date: 2021/01/24/23/21

"""

from flask import render_template,url_for,flash,redirect
from flaskblog import app, db, bcrypt
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [
    {
        'author':'Mike',
        'title':'Flask Post 1',
        'content':'First Flask blog post.',
        'date_posted':'22, Jan, 2021'
    },
    {
        'author':'Jim',
        'title':'Flask Post 2',
        'content':'Second Flask blog post.',
        'date_posted':'23, Jan, 2021'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title = 'About')


@app.route('/register',methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_passwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you are able to login','success')
        return redirect(url_for('login'))
    return render_template('register.html',title="Register",form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.',
                  'danger')
    return render_template('login.html',title="Login",form=form)
