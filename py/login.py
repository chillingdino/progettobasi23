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
	
@login.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login.log'))
#admin-----------------------------------------------------------------------------------------
#----------------------------------------------------------impostazioni tabelle ----------------------

#homepage admin, permette di cambiare i ruoli
@login.route('/private/admin', methods= ['GET', 'POST'])#corretto
@login_required
def admin():
	if current_user.ruolo == 'admin':
		users = get_all_users()
		jusers = json.dumps([dict(ix) for ix in users],  default=str)
		if request.method == 'GET':
			return render_template('admin.html', value= current_user.nome, all_users = jusers)
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
	
#------------------prof----------------------	
#ruolo: prof, homepage professore
@login.route('/private/professore', methods=['GET','POST'])#corretto
@login_required
def professore():
	if current_user.ruolo =='professore':
		jprove = get_jprove_prof(current_user.id)
		jesami = get_jesami_prof(current_user.id)
		if request.method == 'GET':
			return render_template('professore.html', value='current_user.nome', prove=jprove, esami=jesami )
	else:
		return redirect(url_for('login.log'))
	
#ruolo: prof, creazioni prove
@login.route('/private/creazioneProve', methods= ['GET', 'POST'])#corretto
@login_required
def prof_prove():
	if current_user.ruolo == 'professore':
		if request.method == 'GET':
			ris = get_jprove_prof(current_user.id)
			return render_template('creazioneProve.html', prove=ris)
		else:
			#POST
			data = request.form
			try:
				insert_prova(data, current_user.id)
				flash("Inserimento riuscito", category="alert alert-success")
			except Exception as e: 
				print(e)
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.prof_prove'))
	else:
			return redirect(url_for('login.log'))

#rouolo: prof, pagina per creare esami
@login.route('/private/creazioneEsami', methods= ['GET', 'POST'])#corretto
@login_required
def prof_esami():
	if current_user.ruolo == 'professore':
		if request.method == 'GET':
			ris = get_jesami_prof(current_user.id)
			return render_template('creazioneEsami.html', esami=ris)
		else:
			#POST
			try:
				print("utente: " + current_user.id)
				insert_esami(request.form, current_user.id)

				#insert_prove(data, current_user)
				flash("Inserimento riuscito", category="alert alert-success")
			except Exception as e:
				print(e)
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.professore'))
	else:
			return redirect(url_for('login.log'))

#ruolo: prof, registrazione prova studente
@login.route('/private/regVotoProve', methods= ['GET', 'POST'])#corretto
@login_required
def prof_registrazioneVotoProve():
	if current_user.ruolo == 'professore': 
		if request.method == 'GET':
			return render_template('regProve.html')
		else:
			#POST
			data = request.form
			print(data)
			try:
				insert_votoProva(data)
				#insert_prove(data, current_user)
				flash("Inserimento riuscito", category="alert alert-success")
			except Exception as e:
				print(e)
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.prof_registrazioneVotoProve'))
	else:
			return redirect(url_for('login.log'))

#ruolo: prof, registrazione esame studente
@login.route('/private/regEsame', methods= ['GET', 'POST'])#corretto
@login_required
def prof_registrazioneVotoEsame():
	if current_user.ruolo == 'professore': 
		if request.method == 'GET':
			ris = get_stud_reggistrazione_esame_possibile(current_user.id)
			return render_template('regEsame.html', corsi=ris)
		else:
			#POST
			data = request.form
			try:
				insert_esami_superati(data)
				#insert_prove(data, current_user)
				flash("Inserimento riuscito", category="alert alert-success")
			except:
				flash("Errore inserimento", category="alert alert-warning")
			return redirect(url_for('login.prof_registrazioneVotoEsame'))
	else:
			return redirect(url_for('login.log'))

#------------------studente----------------------
	
#roulo: studente, iscrizioni prove 
@login.route('/private/iscrProve', methods=['GET','POST'])#corretto
@login_required
def utente_iscrizoni():
	if current_user.ruolo =='utente':
		jprenotazioni = get_prove_iscrizionePossibile(current_user.id)
		print(jprenotazioni)
		if request.method == 'GET':
			return render_template('iscrProve.html', value='current_user.nome', pronatazioni=jprenotazioni)
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
@login.route('/private/user', methods=['GET', 'POST'])
@login_required
def utente():
    if current_user.ruolo == 'utente':
        jprove = get_jiscrizione_prova(current_user.id)
        jesami = get_jesami_superati(current_user.id)
        if request.method == 'GET':
            return render_template('user.html', value='current_user.nome', prove=jprove, esami=jesami)
    else:
        return redirect(url_for('login.log'))





#dato appello ritorna tutti coloro che lo hanno passato
@login.route('/private/risAppello') #corretto
@login_required
def risultato_appello():
	if current_user.ruolo=='professore':
		try: 
			my_var = request.args.get('my_var', None)
			x = get_result_prova(my_var)
			return render_template('risAppello.html', ris = x )
		except:
			return render_template('risAppello.html' )
	else:
		return redirect(url_for('login.log'))



#informazioni prove e esami, nome prof, date, magari anche durata(?)
@login.route('/private/infoEsame')
@login_required
def info_esami():
	if current_user.ruolo =='utente' or current_user.ruolo=='professore':
		try: 
			my_var = request.args.get('my_var', None)
			x = get_result_prova(my_var)
			return render_template('infoEsame.html', ris = x )
		except:
			return render_template('infoEsame.html' )
	else:
		return redirect(url_for('login.log'))