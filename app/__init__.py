from flask import Flask, redirect, url_for, render_template, request, flash, session

from werkzeug.security import generate_password_hash, check_password_hash

import database

from flask_bootstrap import Bootstrap5

app = Flask(__name__)

@app.before_request
def before_request():
    path = request.path
    if not 'user' in session and path != "/login" and path != "/logout" and path != "/register":
        flash("¡Inicia sesión para continuar!", "danger")
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        if not password == password_confirm:
            flash("Ambas constraseñas no coinciden intente nuevamente", "danger")
            return redirect("/register")
        
        try:
            hash_password = generate_password_hash(password)
            database.create_user(email, hash_password)
            flash("¡Usuario registrado correctamente!", "success")
            return redirect("/login")
        except Exception as ex:
            flash("¡Error al registrar usuario!", "danger")
            return redirect("/register")
        
    return render_template("auth/register.html")

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = database.get_user_by_email(email)
            if user == None:
                flash("¡Correo y/o contraseña incorrecta!", "danger")
                return redirect("/login")
            
            if not check_password_hash(user[1], password):
                flash("¡Correo y/o contraseña incorrecta!", "danger")
                return redirect("/login")
            
            session["user"] = email
            return redirect("/dashboard")
            
        except Exception as ex:
            print(ex)
    
    return render_template("auth/login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("¡Cerraste sesión correctamente!", "success")
    return redirect("/login")

@app.route("/dashboard")
def get_dashboard():
    return render_template("dashboard.html", user=session["user"])


def create_app(config):
    Bootstrap5(app)
    app.config.from_object(config)
    return app