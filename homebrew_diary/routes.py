from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user

from homebrew_diary import app, db
from homebrew_diary.forms import LoginForm, RegistrationForm
from homebrew_diary.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', pagetitle="derp")

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/brews')
def brews():
    return render_template('brews.html')

@app.route('/tastings')
def tastings():
    return render_template('tastings.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))