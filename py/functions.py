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

#crea l'esame
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
	return db.engine.execute("INSERT INTO Prove(codProva, esame, docenteReferente, tipoProva,dataProva ) VALUES (%s,%s, %s, %s, %s)", codProva, esame, docenteReferente, tipoProva, dataProva)

def insert_prenotazioni_prove(data):
    risultato = data['risultato']
    codProva = str(data['codProva'])
    studente = data['studente']

    return db.engine.execute("""
        INSERT INTO Iscrizione_prove(risultato, prova, studente)
        VALUES (%s, %s, %s)
    """, risultato, codProva, studente)

def get_jiscrizione_prova(cfutente):
	result = db.engine.execute("SELECT * FROM Iscrizione_prove ip NATURAL JOIN Prove p WHERE ip.studente = %s", cfutente).fetchall()
	jiscrizioni = json.dumps([dict(ix) for ix in result],  default=str)
	
	return jiscrizioni


def get_jesami_prof(prof):
	result = db.engine.execute("SELECT * FROM Esami es NATURAL JOIN Prove p WHERE es.docente = %s", prof).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	return jresult

def get_jprove_prof(prof):
	result = db.engine.execute("SELECT * FROM Esami es NATURAL JOIN Prove p WHERE es.docente = %s", prof).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	return jresult


def get_jrisulato_prove(cfutente):
	result = db.engine.execute("SELECT * FROM Risulato_prove r WHERE ip.studente = %s", cfutente).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	
	return jris

#per gli esami del prof, tutti gli studenti che hanno passato una prova con richiesta o completo
def get_stud_reggistrazione_esame_possibile(prof):
	result = db.engine.execute("SELECT * FROM Risulato_prove r Join Prove p on r.codProva=p.codProva join Esami e on e.codEsame=p.esame WHERE e.docenteReferente = %s and r.voto>18 and (p.completo=true or richestoSuperamentoCodProva in not null) and GETDATE()<p.dataScandenza", prof).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	
	return jris
#reggistra voto a studente
def insert_esami_superati(data):
	return db.engine.execute("INSERT INTO Esami_superati(esame, studente, voto ) VALUES (%s,%s, %s,)", data["codProva"], data["esame"], data["voto"])


def get_jesami_superati(cfutente):
	result = db.engine.execute("SELECT * FROM Esami_superati es WHERE es.studente = %s", cfutente).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	
	return jris
#################### togliere
