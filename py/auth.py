from flask import Flask, request, url_for, redirect, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime
from .create import db
from .create import login_manager
from .create import bcrypt


class User(UserMixin):
    def __init__(self, codfiscale,nome,cognome,eta,sesso,cellulare, email, pwd, ruolo, active =True):
        self.id = codfiscale
        self.nome = nome
        self.cognome = cognome
        self.eta = eta
        self.email = email
        self.sesso = sesso
        self.cellulare = cellulare
        self.pwd = pwd
        self.ruolo = ruolo
        self.active = active
        
def encode_pwd(pwd):
    pw_hash = bcrypt.generate_password_hash(pwd, 10).decode("utf-8")
    return pw_hash

def decode_pwd(hash_pwd,real_pwd):
    return bcrypt.check_password_hash(hash_pwd, real_pwd)

def get_user_by_email(email):
    ris = db.engine.execute('SELECT * FROM Utenti WHERE email = %s', email)
    user = ris.fetchone()
    return User(user.codfiscale,user.nome,user.cognome,user.eta, user.email,user.sesso,user.cellulare, user.password)

@login_manager.user_loader
def load_user(codfiscale):
    try:
        ris = db.engine.execute('SELECT * FROM Utenti WHERE codfiscale = %s', codfiscale)
        user = ris.fetchone()
        return User(user.codfiscale,user.nome,user.cognome,user.eta, user.email,user.sesso,user.cellulare, user.password, user.ruolo)
    except:
        return ""


@login_required
def jsonuser(user):
    response = {   'id' : user.id,
                    'nome' : user.nome,
                    'cognome' : user.cognome,
                    'eta' : user.eta,
                    'sesso' : user.email,
                    'cellulare' : user.cellulare,
                    'pwd' : user.pwd,
                    'ruolo': user.ruolo

                }
    return response