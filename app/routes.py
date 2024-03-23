from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required

from app.models import User, UserData
from app.forms import LoginForm, RegistrationForm, DataForm
from app.crud import post_data, get_data, update_data, delete_data, get_one_article
from app import app, db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/send', methods=['GET', 'POST'])
@login_required
def send_article():
    form = DataForm()
    if form.validate_on_submit():
        post_data(title=form.title.data, text=form.data.data, user_id=current_user.id)
        return redirect(url_for('get_articles'))
    return render_template('send_data.html', title='post_data', form=form)


@app.route('/get', methods=['GET'])
@login_required
def get_articles():
    user_id=current_user.id
    data = get_data(user_id=user_id)
    return render_template('get_data.html', title='get_data', data=data)
    pass


@app.route("/update/<int:article>", methods=["GET", "POST"])
@login_required
def update_articles(article):
    user_id = current_user.id
    form = DataForm()
    if form.validate_on_submit():
        update_data(data_id=article, title=form.title.data, text=form.data.data, user_id=user_id)
        return redirect(url_for('get_articles'))
    else:
        prev_data = get_one_article(user_id=user_id, data_id=article)
        form.title.data = prev_data[0]
        form.data.data = prev_data[1]
    return render_template('update_data.html', title='post_data', form=form)


@app.route('/delete/<int:article>', methods=['GET', 'POST'])
@login_required
def delete_article(article):
    user_id = current_user.id
    delete_data(user_id=user_id, data_id=article)
    return redirect(url_for('get_articles'))