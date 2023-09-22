from .create import db
from .auth import *
import json
import re
from datetime import datetime


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


#################### 

#crea l'esame
def insert_esami(data, docenteR):
	codeEsame = data['codesame']
	materia = data["materia"]
	docente = docenteR #data['docenteaggiuntivo']
	print("insert 2 : " +  docenteR)
	#print(docente)

	return db.engine.execute("INSERT INTO Esami(codEsame, materia, docenteReferente, docente ) VALUES (%s,%s, %s, %s)", codeEsame, materia, docenteR, docenteR)


def insert_prova(data, user): 
	codProva = data.get('codprova')
	esame = data.get('esame')
	nomeprova = data.get('nomeprova')
	tipoProva = data.get('tipoprova')
	durata = data.get('durata')
	descrizione= data.get('tipoprova')
	print(descrizione)
	dataProva = data.get('dataprova')
	completo = bool(data.get('completo'))
	datascandenza = data.get('datascadenza')
	richiesta = data.get('richiestosuperamentododprova')
	durata = data.get('durata')
	return db.engine.execute("INSERT INTO Prove(codProva, nomeProva, esame, docenteReferente, descrizione,  tipoProva,dataProva, dataScandenza, richestoSuperamentoCodProva, completo ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", codProva, nomeprova, esame, user, descrizione,durata,  tipoProva, dataProva, datascandenza, richiesta, completo)

def insert_prenotazioni_prove(data, user):
	print(data)

	codProva = str(data['codProva'])
	
	return db.engine.execute("""
        INSERT INTO Iscrizione_prove(prova, studente)
        VALUES (%s, %s)
    """, codProva, user)


#- --- - - - -- -  -- - - - - - - - - - -- - - - - GET: 

def get_jiscrizione_prova(cfutente):
	result = db.engine.execute("SELECT * FROM Iscrizione_prove as ip LEFT JOIN Prove as p ON ip.prova=p.codProva  WHERE ip.studente = %s", cfutente).fetchall()
	jiscrizioni = json.dumps([dict(ix) for ix in result],  default=str)
	return jiscrizioni


def get_jesami_prof(prof):
	result = db.engine.execute("SELECT * FROM Esami es WHERE es.docenteReferente = %s OR es.docente= %s", prof, prof).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	#print(jresult)
	return jresult

def get_jprove_prof(prof):
	print(prof)
	result = db.engine.execute("SELECT p.codProva, p.nomeProva, p.dataProva FROM Esami es RIGHT JOIN Prove p ON es.codEsame=p.esame WHERE es.docente = %s OR es.docenteReferente=%s", prof, prof).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	return jresult

#ritorna prove a cui l'utente non si e` anora iscritto
def get_prove_iscrizionePossibile(cfutente):
	result = db.engine.execute("SELECT * FROM Prove AS p WHERE p.dataScandenza > CURRENT_TIMESTAMP AND p.codProva NOT IN ( SELECT ip.prova FROM Iscrizione_prove AS ip WHERE ip.studente = %s);", cfutente).fetchall()
	jresult = json.dumps([dict(ix) for ix in result],  default=str)
	return jresult




def get_jrisulato_prove(cfutente):
	result = db.engine.execute("SELECT * FROM Risulato_prove r WHERE ip.studente = %s", cfutente).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	
	return jris

#per gli esami del prof, tutti gli studenti che hanno passato una prova con richiesta o completo
def get_stud_reggistrazione_esame_possibile(prof):
	result = db.engine.execute("SELECT * FROM Risulato_prove as r LEFT JOIN Prove as p on r.prova=p.codProva join Esami e on e.codEsame=p.esame WHERE e.docenteReferente = %s and CAST(r.voto AS INT)>=18 and (p.completo=true or richestoSuperamentoCodProva is not null) and NOW()<p.dataScandenza", prof).fetchall()
	jris = json.dumps([dict(ix) for ix in result],  default=str)
	
	return jris
	
#reggistra voto a studente
def insert_esami_superati(data):
	db.engine.execute("INSERT INTO Esami_superati(esame, studente, voto ) VALUES (%s,%s, %i)", data["codProva"], data["studente"], data["voto"])

def insert_votoProva(data):
	db.engine.execute("INSERT INTO Risulato_prove(prova, voto, studente ) VALUES (%s,%s, %s)", data["codProva"], data["voto"],  data["studente"] )

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
