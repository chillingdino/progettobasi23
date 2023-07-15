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
		email = str(details['email'])
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

#admin-----------------------------------------------------------------------------------------
@login.route('/private/admin')
@login_required
def admin():
	if current_user.ruolo == 'admin':
			jprenotazioni = get_jprenotazionilezioni()
			return render_template('admin.html', value= current_user.nome, prenotazioni= jprenotazioni)

#----------------------------------------------------------impostazioni tabelle ----------------------

@login.route('/private/admin/roles', methods= ['GET', 'POST'])
@login_required
def role():
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




#visualizzazione e creazione lezioni
@login.route('/private/lezioni', methods= ['GET', 'POST'])
@login_required
def adminevents():
	if current_user.ruolo == 'admin' or current_user.ruolo == 'professore':
		if request.method == 'GET':
			jprenotazioni = get_jprenotazionilezioni()
			return render_template('events.html', value= current_user.nome, prenotazioni= jprenotazioni)
		else:
			#POST
			#ADD EVENT
			try: 
				details = request.form
				insert_prenotazionilezioni(details)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.adminevents'))
	else:
			return redirect(url_for('login.log'))

@login.route('/private/admin/aule', methods= ['GET', 'POST'])
@login_required
def adm_aule():
	if current_user.ruolo == 'admin':
		if request.method == 'GET':
			auleuni = get_jaule()
			return render_template('admin_aule.html',aule= auleuni)
		else:
			#POST
			data = request.form
			try:
				insert_aule(data)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento aula", category="alert alert-warning")
			
			return redirect(url_for('login.adm_aule'))
	else:
			return redirect(url_for('login.log'))

@login.route('/private/corsi', methods= ['GET', 'POST'])
@login_required
def adm_corsi():
	if current_user.ruolo == 'admin' or current_user.ruolo == 'professore':

		if request.method == 'GET':
			corsiuni = get_jcorsi()
			
			return render_template('admin_corsi.html', corsi=corsiuni)
		else:
			#POST
			data = request.form
			try:
				insert_corsi(data, current_user)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")
			
			return redirect(url_for('login.adm_corsi'))
	else:
			return redirect(url_for('login.log'))


@login.route('/private/admin/edifici', methods= ['GET', 'POST'])
@login_required
def adm_edifici():
	if current_user.ruolo == 'admin':
		if request.method == 'GET':
			
			edificiuni = get_jedifici()
			return render_template('admin_edifici.html', edifici= edificiuni)
		else:
			#POST
			data = request.form
			try:
				insert_edifici(data)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")

			return redirect(url_for('login.adm_edifici'))
	else:
			return redirect(url_for('login.log'))

#prof------------------------------------------------------------------------------------------

@login.route('/private/professore')
@login_required
def professore():
	if current_user.ruolo == 'professore':
		uniattivita = get_jprenotazionilezioni()
		return render_template('professore.html', value=current_user.nome, prenotazioni= uniattivita)


@login.route('/private/professore/statistiche')
@login_required
def profstat():
	if current_user.ruolo == 'professore':
		
		p = get_prenotati()
		c = get_jcorsi()
		i = get_jcorsiprenotazioni()
		return render_template('prof_statistiche.html', corsi=c, lezioni= p, iscritti=i)
	else:
		return redirect(url_for('login.log'))

#-----------------------------------------------------------------------------------------------
@login.route('/private/user', methods=['GET','POST'])
@login_required
def utente():
	if current_user.ruolo =='utente':
		jprenotazioni = get_jprenotazionilezioni()
		if request.method == 'GET':
			return render_template('user.html', value='current_user.nome', prenotazioni=jprenotazioni)
		else:
			details = request.form
			res = prenotazione_posti(details, current_user.id)
			if (not res):
				flash("Lezione non trovata", category="alert alert-warning")
			else:
				flash("Pronatazione avvenuta con successo", category="alert alert-success")
			return redirect(url_for('login.utente'))

	else:
		return redirect(url_for('login.log'))

@login.route('/private/user/lezioni_prenotate')
@login_required
def lezioni_prenotate():
	if current_user.ruolo =='utente':
		jprenotazioni = get_prenotazioniutente(current_user.id)
		return render_template('lezioni_prenotate.html', value='current_user.nome', prenotazioni=jprenotazioni)
	else:
		return redirect(url_for('login.log'))

@login.route('/private/user/iscrizione_corsi',methods=['GET','POST'])
@login_required
def iscrizione_corsi():
	if current_user.ruolo =='utente':
		if request.method == 'GET':
			corsiuni = get_jcorsi()
			iscrizioni = get_jiscrizioni(current_user)
			return render_template('iscrizione_corsi.html', value='current_user.nome', corsi=corsiuni, iscrizioni=iscrizioni)
		else:
			details = request.form
			try:
				iscrizione_corso(details, current_user)
				flash("Iscrizione avvenuta con successo", category="alert alert-success")
			except:
				flash("Corso non trovato", category="alert alert-warning")
			return redirect(url_for('login.iscrizione_corsi'))
	else:
		return redirect(url_for('login.log'))

@login.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login.log'))




	
