from flask import render_template, redirect, url_for, flash

from werkzeug.security import generate_password_hash, check_password_hash

from database.db import db

from database.models import User

from auth.forms import RegisterForm, LoginForm

from flask_login import login_user, logout_user


def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(email=form.email.data).first()

        if existing:

            flash("Email already exists", "danger")

            return redirect(url_for("register"))

        hashed = generate_password_hash(form.password.data)

        user = User(

            username=form.username.data,

            email=form.email.data,

            password=hashed

        )

        db.session.add(user)

        db.session.commit()

        flash("Registration Successful", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):

            login_user(user)

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html", form=form)


def logout():

    logout_user()

    return redirect(url_for("login"))