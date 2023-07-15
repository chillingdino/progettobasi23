CREATE TYPE role as ENUM('utente', 'professore', 'admin');
CREATE TYPE valoreProva as ENUM('bonus', 'voto', 'idoneo', 'insuf')

CREATE TABLE Utenti(
	codFiscale varchar(100)  NOT NULL,
	nome		varchar(100) NOT NULL,
	cognome		varchar(100) NOT NULL,
	eta			smallint NOT NULL,
	sesso		smallint NOT NULL,
	cellulare	varchar(50),
	email		varchar(100) UNIQUE NOT NULL,
	password	varchar(100) NOT NULL,
	ruolo		role,
PRIMARY KEY (codFiscale)
);


--esami, reggistrazione prove (tra stud e prove), convalida-prove, prove, appelli, utenti (doc, admin, stud) 

--esami: materia, docente <FK>,
--esami_superati: <fk> esami, fk studente, voto, data_reggistrazione
--esami-prove: <FK> ESAMI, <FK> prove
--prove: <FK> docente-referente , tipo prova <string>,  valoreProva, data_prova, data_scadenza
--iscrizione_prova: risultato <nullable> int, fk prove, fk utente

CREATE TABLE Esami(
    codEsame varchar(50),
    materia varchar(50) not null,
    docente varchar(50) not null,
	PRIMARY KEY (codEsame)
)

CREATE TABLE Esami_superati(
	esame varchar(50) NOT NULL,
	studente varchar(50) NOT NULL,
    voto int not null,
	PRIMARY KEY (esame,studente),
	FOREIGN KEY (studente) REFERENCES Utenti(codFiscale),
	FOREIGN KEY (esame) REFERENCES Esame(codEsame)
);

CREATE TABLE Esami_prove(
	esame varchar(50) NOT NULL,
	prova varchar(50) NOT NULL,
	PRIMARY KEY (esame,prova),
	FOREIGN KEY (prova) REFERENCES Prove(codProva),
	FOREIGN KEY (esame) REFERENCES Esame(codEsame)
);

CREATE TABLE Prove(
    codProva varchar(50),
    docenteReferente varchar(50),
    tipoProva varchar(50),
    dataProva timestamp not null,
    dataScandenza timestamp not null,
    FOREIGN KEY (studente) REFERENCES Utenti(codFiscale),
	FOREIGN KEY (esame) REFERENCES Esame(codEsame)
)

CREATE TABLE Iscrizione_prova(
	risultato int,
	prove varchar(50),
	studente varchar(50),
	FOREIGN KEY (prove) REFERENCES Prove(codProva),
	FOREIGN KEY (studente) REFERENCES Utenti(codFiscale)
)


