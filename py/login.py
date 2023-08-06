from flask import Flask, Blueprint, render_template, flash, url_for, redirect, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from .create import db
from .auth import *
from .functions import *
import json

#gestione pagina di login(richiamata da href in index)
login = Blueprint('login', __name__)

@login.route('/', methods=['GET', 'POST'])
def log():
	if request.method == "POST":
		details = request.form
		#email = form.email.data
		#pw = form.email.password
		email = details['email']
		pw = details['password']

		result = db.engine.execute("SELECT * FROM Utenti WHERE (email = %s)", (email))
		queryUser = result.fetchone()
		
		if queryUser:
			if decode_pwd(queryUser.password,pw):
				user = User(queryUser.codfiscale,queryUser.nome,queryUser.cognome,queryUser.eta, queryUser.email,queryUser.sesso,queryUser.cellulare, queryUser.password, queryUser.ruolo)
				login_user(user)
				role = current_user.ruolo
				flash("Sei loggato", category='alert alert-success')
				return redirect(url_for('login.'+ role))
			else:
				flash("Password sbagliata", category="alert alert-warning")
				return redirect(url_for('login.log'))
		else:
			flash("Questa email non e`registrata", category="alert alert-warning")
			return redirect(url_for('login.log'))
	else:
		return render_template('login.html')  

#permetto il log-out
@login.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login.log'))

#admin-----------------------------------------------------------------------------------------
#----------------------------------------------------------impostazioni tabelle ----------------------

#homepage di admin per cambiare ruoli
@login.route('/private/admin', methods= ['GET', 'POST'])
@login_required
def admin():
	if current_user.ruolo == 'admin':
		users = get_all_users()
		jusers = json.dumps([dict(ix) for ix in users],  default=str)
		if request.method == 'GET':
			return render_template('admin_roles.html', value= current_user.nome, all_users = jusers)
		else:
			details = request.form
			try:
				adm_changerole(details)
				flash("Cambio ruolo riuscito", category="alert alert-success")
			except:
				flash("Errore cambio ruolo", category="alert alert-warning")
			return redirect(url_for('login.role'))
	else:
			return redirect(url_for('login.log'))
	
#pagina per creare esami
@login.route('/private/creazioneEsami', methods= ['GET', 'POST'])
@login_required
def creazioneEsami():
	if current_user.ruolo == 'professore':
		if request.method == 'GET':
			ris = get_jesami_prof()
			return render_template('professore.html', corsi=ris)
		else:
			#POST
			data = request.form
			try:
				insert_esami(data, current_user.id)
				#insert_prove(data, current_user)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.adm_corsi'))
	else:
			return redirect(url_for('login.log'))
	
#reggistrazione voto studente
@login.route('/private/reggistrazioneEsamiSuperati', methods= ['GET', 'POST'])
@login_required
def reggistrazioneEsamiSuperati():
	if current_user.ruolo == 'professore':
		if request.method == 'GET':
			ris = get_stud_reggistrazione_esame_possibile()
			return render_template('admin_corsi.html', corsi=ris)
		else:
			#POST
			data = request.form
			try:
				insert_esami_superati(data)
				#insert_prove(data, current_user)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.adm_corsi'))
	else:
			return redirect(url_for('login.log'))

#creazione prove
@login.route('/private/prove', methods= ['GET', 'POST'])
@login_required
def prof_prove():
	if current_user.ruolo == 'professore':
		if request.method == 'GET':
			ris = get_jesami_prof()
			return render_template('admin_corsi.html', corsi=ris)
		else:
			#POST
			data = request.form
			try:
				insert_prova(data, current_user.id)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.adm_corsi'))
	else:
			return redirect(url_for('login.log'))
	
#iscrizioni a prove da perte di studente
@login.route('/private/iscrzioneProve', methods=['GET','POST'])
@login_required
def utente_iscrizoni():
	if current_user.ruolo =='utente':
		jprenotazioni = get_jiscrizione_prova(current_user.id)
		if request.method == 'GET':
			return render_template('user.html', value='current_user.nome', prenotazioni=jprenotazioni)
		else:
			details = request.form
			res = insert_prenotazioni_prove(details, current_user.id)
			if (not res):
				flash("Lezione non trovata", category="alert alert-warning")
			else:
				flash("Pronatazione avvenuta con successo", category="alert alert-success")
			return redirect(url_for('login.utente'))
	else:
		return redirect(url_for('login.log'))
	
#pagina inizile user
@login.route('/private/utente', methods=['GET','POST'])
@login_required
def utente():
	if current_user.ruolo =='utente':
		jprove = get_jiscrizione_prova(current_user.id)
		jproveall = get_all_prove()
		jesami = get_jesami_superati(current_user.id)
		if request.method == 'GET':
			return render_template('user.html', value='current_user.nome', prove=jprove, esami=jesami, jproveall=jproveall )
	else:
		return redirect(url_for('login.log'))

#dato appello ritorna tutti coloro che lo hanno passato
@login.route('/private/risultatoAppello')
@login_required
def risultato_appello():
	if current_user.ruolo =='utente' or current_user.ruolo=='professore':
		my_var = request.args.get('my_var', None)
		x = get_result_prova(my_var)
		return render_template('risultatiAppello.html', ris = x )
	else:
		return redirect(url_for('login.log'))
#----old
