from models import User, Post

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
    },
    {
        'title': 'Reaping Off',
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
        flash(
            f'Account created for {form.username.data} successfully!', 'success')
        return redirect(url_for('home'))
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