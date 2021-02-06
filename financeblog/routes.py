from flask import render_template, url_for, flash, redirect
from financeblog import app, db, bcrypt
from financeblog.models import User, Post
from financeblog.forms import RegistrationForm, LoginForm

posts = [
    {
        'title': 'Getting Started',
        'content': 'Here is why I may not see eye to eye with most of the so called millionaires out there whether self made or otherwise They never tell you what they actually realistically did to make their first dollar later snowballing into millions.',
        'date_posted': 'Jan 21, 2021'
    },

    {
        'title': 'Setting Up',
        'content': 'Millionaires out there whether self made or otherwise They never tell you what they actually realistically did to make their first dollar later snowballing into millions.',
        'date_posted': 'Jan 21, 2021'
    },
    {
        'title': 'Down and Right',
        'content': 'Millionaires out there whether self made or otherwise They never tell you what they actually realistically did to make their first dollar later snowballing into millions.',
        'date_posted': 'Jan 21, 2021'
    },

    {
        'title': 'Lift-Off',
        'content': 'Millionaires out there whether self made or otherwise They never tell you what they actually realistically did to make their first dollar later snowballing into millions.',
        'date_posted': 'Jan 21, 2021'
    }
]


@ app.route('/')
@ app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@ app.route('/about')
def about():
    return render_template('about.html')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            'Your account has been created successfully! Login to continue', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@ app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@log.com' and form.password.data == 'password':
            flash('You have been logged in successfully', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')     
    return render_template('login.html', title='Login', form=form)