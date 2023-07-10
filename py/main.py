from flask import Flask, request, url_for, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_bcrypt import Bcrypt
import json
import collections
import datetime
app = Flask(__name__)

app.run(debug=True)
 
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:Daniele123@localhost:5432/musicstream'
db = SQLAlchemy(app)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, codfiscale,nome,cognome,eta,sesso,cellulare, email, pwd, active =True):
        self.id = codfiscale
        self.nome = nome
        self.cognome = cognome
        self.eta = eta
        self.email = email
        self.sesso = sesso
        self.cellulare = cellulare
        self.pwd = pwd
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
        return User(user.codfiscale,user.nome,user.cognome,user.eta, user.email,user.sesso,user.cellulare, user.password)
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
                    'pwd' : user.pwd

                }
    return response

##
#pagina iniziale
##
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        email = str(details['email'])
        pw = details['password']
        
        result = db.engine.execute("SELECT * FROM Utenti WHERE (email = %s)", (email))
        queryUser = result.fetchone()

        if queryUser is not None:
            user = User(queryUser.codfiscale,queryUser.nome,queryUser.cognome,queryUser.eta, queryUser.email,queryUser.sesso,queryUser.cellulare, queryUser.password)
            login_user(user)

            return redirect(url_for('showprofile')) 
            
    else:
        return render_template('index.html', output = "riprovare l' accesso")  
   
            
@app.route('/private_user/',methods=['GET', 'POST'])
@login_required
def showprofile():

    if request.method == "GET":
        return render_template('user.html', output = current_user.id)
        
  
    else:
        
        return redirect(url_for('showprofileutenti'))




@app.route('/reg',methods=['GET', 'POST'])
def addprofile():
    if request.method == "GET":
        return render_template('profileReg.html')
    else:  
        details = request.form
        codfisc = details['codfiscale']
        firstName = details['fname']
        lastName = details['lname']
        age = details['age']
        sex = details['sex']
        phonenumber = details['phone']
        email = details['email']
        password = details['password']
        try:
            pw_crypt = encode_pwd(password)
            db.engine.execute("INSERT INTO Utenti VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (codfisc, firstName,lastName ,age ,sex ,phonenumber,email,pw_crypt))
            return render_template('profileReg.html', output = "new account reg already")
        except:
            return render_template('profileReg.html', output = "Error probably acc already present")

if __name__ == '__main__':
    app.run()
