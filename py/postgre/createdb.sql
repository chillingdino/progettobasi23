
CREATE TYPE ruolo as ENUM('utente', 'professore', 'admin');
CREATE TYPE valoreProva as ENUM('bonus', 'voto', 'idoneo', 'insuf');

CREATE TABLE Utenti(
	codFiscale varchar(100)  NOT NULL,
	nome		varchar(100) NOT NULL,
	cognome		varchar(100) NOT NULL,
	eta			smallint NOT NULL,
	sesso		smallint NOT NULL,
	cellulare	varchar(50),
	email		varchar(100) UNIQUE NOT NULL,
	password	varchar(100) NOT NULL,
	ruolo		ruolo,
PRIMARY KEY (codFiscale)
);


--esami, reggistrazione prove (tra stud e prove), convalida-prove, prove, appelli, utenti (doc, admin, stud) 

--esami: materia, docente <FK>,
--esami_superati: <fk> esami, fk studente, voto, data_reggistrazione
--prove: <FK> docente-referente , tipo prova <string>,  valoreProva, data_prova, data_scadenza
--iscrizione_prova: risultato <nullable> int, fk prove, fk utente

CREATE TABLE Esami(
    codEsame varchar(50) not null,
    materia varchar(50) not null,
    docenteReferente varchar(50) not null,
	docente varchar(50),
	FOREIGN KEY (docenteReferente) REFERENCES Utenti(codFiscale),
	FOREIGN KEY (docente) REFERENCES Utenti(codFiscale),
	PRIMARY KEY (codEsame)
);

CREATE TABLE Esami_superati(
	esame varchar(50) NOT NULL,
	studente varchar(50) NOT NULL,
    voto int not null,
	PRIMARY KEY (esame,studente),
	FOREIGN KEY (studente) REFERENCES Utenti(codFiscale),
	FOREIGN KEY (esame) REFERENCES Esami(codEsame)
);

CREATE TABLE Risulato_prove(
	codProva varchar(50) not null,
	voto varchar(50) not null,
	studente varchar(50) not null,
	FOREIGN KEY (prova) REFERENCES Prove(codProva),
	FOREIGN KEY (studente) REFERENCES Utenti(codFiscale)
)

CREATE TABLE Prove(
    codProva varchar(50) not null,
  	esame varchar(50) not null,
    docenteReferente varchar(50),
    tipoProva varchar(50),
    dataProva timestamp not null,
    dataScandenza timestamp not null,
	richestoSuperamentoCodProva varchar(50),
	completo boolean not null,
  	PRIMARY KEY (codProva),
	FOREIGN KEY (esame) REFERENCES Esami(codEsame)
);

CREATE TABLE Iscrizione_prove(
	risultato int,
	prova varchar(50),
	studente varchar(50),
  	PRIMARY KEY (prova,studente),
	FOREIGN KEY (prova) REFERENCES Prove(codProva),
	FOREIGN KEY (studente) REFERENCES Utenti(codFiscale)
);

CREATE TRIGGER ControlloIscrizioneProva
BEFORE INSERT ON Iscrizione_prove
WHEN (EXISTS SELECT * FROM Prove p join Risulato_prove pr on codProva=richestoSuperamentoCodProva WHERE (new.prova=p.codProva and pr.student) OR p.richestoSuperamentoCodProva=null)
BEGIN
RETURN NULL
END;

CREATE TRIGGER ControlloCreazioneEsame
BEFORE INSERT ON Prove
WHEN (NOT EXISTS SELECT * FROM Esami WHERE new.prova=Esami.codEsame and (new.docenteReferente=Esami.docente OR new.docenteReferente=Esami.docenteReferente)
BEGIN 
RETURN NULL
END;

