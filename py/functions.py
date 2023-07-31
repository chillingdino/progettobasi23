from .create import db
from .auth import *
import json
import re

def get_all_users():
	users = db.engine.execute("SELECT codfiscale, nome, cognome, ruolo FROM Utenti ")
	queryUser = users.fetchall()
	return queryUser

def check_password(password):
	length_errore = len(password) < 8
	digit_errore = re.search(r"\d", password) is None
	uppercase_errore = re.search(r"[A-Z]", password) is None
	lowercase_errore = re.search(r"[a-z]", password) is None

	errore = not(length_errore or digit_errore or uppercase_errore or lowercase_errore)

	return errore

def check_email(email):
	regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'
	errore = (re.fullmatch(regexEmail, email))

	return errore

def adm_changerole(data):
	codice_fiscale = data['codfisc']
	ruolo = data['changerole']
	return  db.engine.execute("UPDATE Utenti SET ruolo = %s WHERE codfiscale = %s",ruolo, codice_fiscale)


#################### new: 

def insert_esami(data):
	codeEsame = data['codEsame']
	materia = data['materia']
	docente = data['docente']
	return db.engine.execute("INSERT INTO Esami(codEsame, materia, docente) VALUES (%s,%s, %s)", codeEsame, materia, docente)


def insert_prova(data): 
	codProva = data['codProva']
	esame = data['codEsame']
	docenteReferente = data['docenteReferente']
	tipoProva = data['tipoProva']
	dataProva = data['dataProva']
	return db.engine.execute("INSERT INTO Edifici(codProva, esame, docenteReferente, tipoProva,dataProva ) VALUES (%s,%s, %s, %s, %s)", codProva, esame, docenteReferente, tipoProva, dataProva)

def insert_prenotazioni_prove(data):
    risultato = data['risultato']
    codProva = str(data['codProva'])
    studente = data['studente']

    return db.engine.execute("""
        INSERT INTO Iscrizione_prove(risultato, prova, studente)
        VALUES (%s, %s, %s)
    """, risultato, codProva, studente)

def get_jiscrizione_prova(cfutente):
	result = db.engine.execute("SELECT * FROM Iscrizione_prove ip NATURAL JOIN Prove p WHERE pp.utente = %s", cfutente)
	isczione = result.fetchall()
	jiscrizioni = json.dumps([dict(ix) for ix in isczione],  default=str)
	
	return jiscrizioni
#################### togliere


def get_jprenotazionilezioni():
	result_prenotazioni = db.engine.execute("SELECT * FROM Prenotazioni_lezioni")
	prenotazioni = result_prenotazioni.fetchall()
	jprenotazioni = json.dumps([dict(ix) for ix in prenotazioni],  default=str)
	return jprenotazioni
	 
def get_jedifici():
	result_edifici = db.engine.execute("SELECT * FROM edifici ORDER BY codedificio ASC")
	edifici = result_edifici.fetchall()
	jedifici = json.dumps([dict(ix) for ix in edifici],  default=str)
	return jedifici

def get_jaule():
	result_aule = db.engine.execute("SELECT * FROM aule")
	aule = result_aule.fetchall()
	jaule = json.dumps([dict(ix) for ix in aule],  default=str)
	return jaule

def get_jcorsi():
	result_corsi = db.engine.execute("SELECT * FROM corsi")
	corsi = result_corsi.fetchall()
	jcorsi = json.dumps([dict(ix) for ix in corsi],  default=str)
	return jcorsi

def get_jiscrizioni(user):
	result_corsi = db.engine.execute("SELECT c.codcorso, c.nome, c.professore, c.datainizio, c.datafine, c.descrizione FROM Iscrizioni_corsi ic JOIN Corsi c ON ic.corso = c.codcorso WHERE ic.studente = %s ", user.id)
	iscrizioni = result_corsi.fetchall()
	jiscrizioni = json.dumps([dict(ix) for ix in iscrizioni],  default=str)
	return jiscrizioni


def get_prenotazioniutente(cfutente):
	result = db.engine.execute("SELECT pl.codprenotazione,pl.corso,pl.aula,pl.datainizio,pl.durata,pl.maxpresenti,pl.online FROM Prenotazioni_lezioni pl  JOIN Prenotazioni_posti pp ON pl.codprenotazione = pp.lezione  WHERE pp.utente = %s", cfutente)
	prenotazioni = result.fetchall()
	jprenotazioni = json.dumps([dict(ix) for ix in prenotazioni],  default=str)
	
	return jprenotazioni


def insert_edifici(data):
	codedificio = data['codedificio']
	indirizzo = data['indirizzo']
	return db.engine.execute("INSERT INTO Edifici(codedificio, indirizzo) VALUES (%s,%s)", codedificio, indirizzo)

def insert_aule(data):
	codaula = data['codaula']
	capienza = data['capienza']
	edificio = data['edificio']
	piano = data['piano']
	return db.engine.execute("INSERT INTO Aule(codaula, capienza,edificio,piano) VALUES (%s,%s,%s,%s)", codaula,capienza,edificio,piano)

def insert_corsi(data, current_user):
	if current_user.ruolo == 'professore':
		professore = current_user.id
	else:
		professore = data['professore']
	if professore == '':
		return None
	else:
		codcorso = data['codcorso']
		nome = data['nome']
		datainizio = data['datainizio']
		datafine = data['datafine']
		descrizione = data['descrizione']

		return db.engine.execute("INSERT INTO Corsi(codcorso, nome, professore, datainizio, datafine, descrizione) VALUES (%s,%s,%s,%s,%s,%s)", codcorso, nome, professore, datainizio, datafine, descrizione)

def insert_prenotazionilezioni(data):
	codcorso = str(data['codicecorso'])
	codaula = data['codiceaula']
	datainizio = data['datainizio']
	maxpresenti = data['maxpresenti']
	durata = data['durata']
	if codaula == '':
		codaula = None
	try:

		online = data['online']
		
	except:
		online = False
	
	if maxpresenti == '':
		maxpresenti = 0
	return db.engine.execute("INSERT INTO Prenotazioni_lezioni(corso,aula,datainizio,durata,maxpresenti, online) VALUES (%s,%s,%s,%s,%s,%s)", codcorso,codaula,datainizio, durata, maxpresenti, online)
	

def prenotazione_posti(data, user):
	codcorso = data['codcorso']
	data = data['datainizio']
	check = check_posti(codcorso,data)
	if check:
		result_lezione = db.engine.execute("SELECT * FROM Prenotazioni_lezioni WHERE corso = %s AND datainizio = %s", codcorso, data)
		lezione = result_lezione.fetchone()
		try:
			ris = db.engine.execute("INSERT INTO Prenotazioni_posti(utente,lezione) VALUES (%s,%s)", user, lezione[0] )
			return ris
		except:
			return None
		
	else:
		return None

def iscrizione_corso(data, user):
	codcorso = data['codcorso']
	
	return db.engine.execute("INSERT INTO Iscrizioni_corsi(corso,studente) VALUES ( %s,  %s)", codcorso, user.id)


def check_posti(corso, data):
	#controllo se ci sono posti per quella lezione, da controllare lezione online

	try:
		lezione = db.engine.execute("SELECT codprenotazione FROM Prenotazioni_lezioni WHERE corso = %s AND datainizio = %s", corso,data)
		idlezione = lezione.fetchone()[0]
		#controllo se la lezione online allora i posti sono illimitati
		online = db.engine.execute("SELECT online FROM Prenotazioni_lezioni WHERE codprenotazione = %s", idlezione)
		on = online.fetchone()[0]
		if on == '':
			occupati = db.engine.execute("SELECT COUNT(*) FROM Prenotazioni_posti WHERE lezione = %s", idlezione)
			disponibili = db.engine.execute("SELECT maxpresenti FROM Prenotazioni_lezioni WHERE codprenotazione = %s", idlezione)
		
			o = int(occupati.fetchone()[0])
			d = int(disponibili.fetchone()[0])
			if o < d :
				return True
			else:
				return False
		else:
			#online
			return True
	except:
		#da gestire
		return False

def get_prenotati():
	prenotati = db.engine.execute("SELECT pl.corso,pl.aula,pl.datainizio,pl.durata, pl.maxpresenti, pl.online, COUNT(pp.utente) AS prenotati FROM Prenotazioni_posti pp RIGHT JOIN Prenotazioni_lezioni pl ON pp.lezione = pl.codprenotazione GROUP BY pp.lezione, pl.corso, pl.aula, pl.datainizio, pl.durata, pl.maxpresenti, pl.online")
	fetch = prenotati.fetchall()
	jprenotati = json.dumps([dict(ix) for ix in fetch],  default=str)

	return jprenotati

def get_jcorsiprenotazioni():
	prenotati = db.engine.execute("SELECT c.codcorso,c.nome,u.nome AS professore,c.datainizio,c.datafine, COUNT(ic.studente)  AS prenotati, AVG(u2.eta) AS media FROM Iscrizioni_corsi ic RIGHT JOIN Corsi c ON ic.corso = c.codcorso JOIN Utenti u ON c.professore = u.codfiscale JOIN Utenti u2 ON ic.studente = u2.codfiscale  GROUP BY c.codcorso,c.nome,u.nome,c.datainizio,c.datafine")
	fetch = prenotati.fetchall()
	jprenotati = json.dumps([dict(ix) for ix in fetch],  default=str)
	return jprenotati