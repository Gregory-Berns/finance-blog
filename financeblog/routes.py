import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from financeblog import app, db, bcrypt
from financeblog.models import User, Post
from financeblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, logout_user, login_required, current_user



@ app.route('/')
@ app.route('/home')
def home():
    posts=Post.query.all()
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful, check email or password', 'danger')     
    return render_template('login.html', title='Login', form=form)


@ app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    
    output_size = (125,125)
    resized_img = Image.open(form_picture)
    resized_img.thumbnail(output_size)
    resized_img.save(picture_path)

    return picture_fn


@ app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Account information updated successfully', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file = url_for('static', filename='images/post_pics')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@ app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()    
    if form.validate_on_submit():
        if form.post_picture.data:
            image_file=form.post_picture.data
        post=Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='images/post_pics')
    return render_template('create_post.html', title='New Post', form=form)