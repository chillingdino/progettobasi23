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
def insert_esami(data, docente):
	codeEsame = data['codEsame']
	materia = data['materia']
	#docente = data['docente']
	return db.engine.execute("INSERT INTO Esami(codEsame, materia, docente) VALUES (%s,%s, %s)", codeEsame, materia, docente)


def insert_prova(data, user): 
	codProva = data['codProva']
	esame = data['codEsame']
	#docenteReferente = data['docenteReferente']
	tipoProva = data['tipoProva']
	dataProva = data['dataProva']
	return db.engine.execute("INSERT INTO Prove(codProva, esame, docenteReferente, tipoProva,dataProva ) VALUES (%s,%s, %s, %s, %s)", codProva, esame, user, tipoProva, dataProva)

def insert_prenotazioni_prove(data, user):
	print(data)

	codProva = str(data['codProva'])
	
	return db.engine.execute("""
        INSERT INTO Iscrizione_prove(prova, studente)
        VALUES (%s, %s)
    """, codProva, user)

def get_jiscrizione_prova(cfutente):
	result = db.engine.execute("SELECT * FROM Iscrizione_prove as ip LEFT JOIN Prove as p ON ip.prova=p.codProva  WHERE ip.studente = %s", cfutente).fetchall()
	jiscrizioni = json.dumps([dict(ix) for ix in result],  default=str)
	return jiscrizioni


def get_jesami_prof(prof):
	result = db.engine.execute("SELECT * FROM Esami es LEFT JOIN Prove p ON es.codEsame=p.esame  WHERE es.docente = %s", prof).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	return jresult

def get_jprove_prof(prof):
	result = db.engine.execute("SELECT * FROM Esami es LEFT JOIN Prove p ON es.codEsame=p.esame WHERE es.docente = %s", prof).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	return jresult

#ritorna prove a cui l'utente non si e` anora iscritto
def get_prove_iscrizionePossibile(cfutente):
	result = db.engine.execute("SELECT * FROM Prove as p WHERE p.codProva NOT IN (SELECT codProva FROM Iscrizione_prove as p2 WHERE p2.studente=%s)", cfutente).fetchall()
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

#ritorna esami passati dallo studente
def get_jesami_superati(cfutente):
	result = db.engine.execute("SELECT * FROM Esami_superati es WHERE es.studente = %s", cfutente).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	return jris


def get_result_prova(prova):
	result = db.engine.execute("SELECT * FROM Prova p inner join Risulato_prove rp WHERE p.codProva=%s", prova).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	return jris

def get_all_prove_expect_already_iscritto(cfutente):
	result = db.engine.execute("SELECT p.codProva, dataProva, p FROM Prove p WHERE p.dataProva>GETDATE() EXCEPT SELECT * FROM Prove p inner join Iscrizione_prove ip on p.codProva=ip.Prova WHERE ip.studente=%s", cfutente).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	return jris

def get_all_prove():
	result = db.engine.execute("SELECT p.codProva, dataProva, p FROM Prove p WHERE p.dataProva>GETDATE()").fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	return jris
#################### togliere
