import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from financeblog import app, db, bcrypt
from financeblog.models import User, Post
from financeblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, logout_user, login_required, current_user



@ app.route('/')
@ app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
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
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



def save_post_image(post_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(post_picture.filename)
    post_picture_filename = random_hex + f_ext
    post_picture_path = os.path.join(app.root_path, 'static/post_pics', 
                                    post_picture_filename )

    # resizing the picture provided post
    output_size = (840, 580)
    i = Image.open(post_picture)
    i.thumbnail(output_size)
    i.save(post_picture_path)

    return post_picture_filename

#------------Create a post-------------------------------------------
@ app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()    
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data, author=current_user)
        if form.post_picture.data:
            post.post_image=save_post_image(form.post_picture.data)       
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published', 'success')
        return redirect(url_for('home'))
    post_image = url_for('static', filename='post_pics/')
    return render_template('create_post.html', title='New Post', form=form, post_image=post_image, legend='New Post')

#---------------Update a post------------------------------------

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id) -> 'html':
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():    
        post.title=form.title.data
        post.content=form.content.data
        if form.post_picture.data:
            post.post_image = save_post_image(form.post_picture.data)                
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method=='GET': 
        form.title.data = post.title
        form.content.data = post.content
        form.post_picture.data = post.post_image    
    post_image = url_for('static', filename='post_pics/' )
    return render_template('create_post.html', title='Update Post', 
                            form=form, legend='Update Post', 
                            post_image=post_image)


#------------Delete a post-------------------------------------------

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id) -> 'html':
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

#------------Render a post-------------------------------------------
@ app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

#------------Render posts from a specific user-------------------------------------------
@ app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)