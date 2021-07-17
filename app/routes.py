from flask import Flask, render_template, redirect, request, url_for, flash
from app import app, db
from app.models import User, Formacao
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/formacoes')
def index():
    formacoes = Formacao.query.all()
    return render_template('formacoes.html', formacoes=formacoes)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            flash("Email ou senha incorretos", category='is-danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html') #form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form['nome']
        email = request.form['email']
        password = request.form['password']

        if name and email and password:
            user = User(name, email, password)
            try:
                db.session.add(user)
                db.session.commit()
                flash('Usuário cadastrado com sucesso', category='is-success')
                return redirect(url_for('login'))
            except:
                flash('Já existe um usuário cadastrado com este email', category='is-danger')
                return redirect(url_for('register'))
                
    return render_template('register.html')


@app.route("/logout")
#@login_required
def logout():
    logout_user()
    flash('Deslogado')
    return redirect(url_for('login'))

@app.route('/cadastrar_formacao', methods=['GET', 'POST'])
@login_required
def cadastrar_formacao():

    if request.method == 'POST':
        tema = request.form['tema']
        data = request.form['data']
        carga_horaria = request.form['carga']
        formacao = Formacao(tema, carga_horaria, data)

        try:
            db.session.add(formacao)
            db.session.commit()
            flash('Formação cadastrada com sucesso', category='is-success')
            return redirect(url_for('index'))
        except:
            flash('Erro ao cadastrar a formação', category='is-danger')
            return redirect(url_for('cadastrar_formacao'))

    return render_template('cadastrar_formacao.html')

@app.route('/delete/<id>')
def delete(id):

    formacao = Formacao.query.get(id)
    db.session.delete(formacao)
    db.session.commit()
    flash('Formação removida com sucesso', category='is-success')
    return redirect(url_for('index'))