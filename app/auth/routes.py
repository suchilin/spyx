from flask import (render_template, redirect, url_for,
                   request, current_app)
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import login_manager
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    #  if current_user.is_authenticated:
    #      return redirect(url_for('public.index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.get_by_email(email)
        if user is not None:
            error = f'This email {email} is already taken'
        else:
            user = User(email=email, name="",description="")
            user.set_password(password)
            user.save()
            return redirect(url_for('hits.list'))
    return render_template("auth/signup_form.html", form=form, error=error)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hits.list'))
    message=""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('hits.list')
            return redirect(next_page)
        else:
            message="User or password incorrect"
    return render_template('auth/login_form.html', form=form,message=message)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
