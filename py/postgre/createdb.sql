CREATE TYPE role as ENUM('utente', 'professore', 'admin');

CREATE TABLE Utenti(
	codfiscale varchar(100)  NOT NULL,
	nome		varchar(100) NOT NULL,
	cognome		varchar(100) NOT NULL,
	eta			smallint NOT NULL,
	sesso		smallint NOT NULL,
	cellulare	varchar(50),
	email		varchar(100) UNIQUE NOT NULL,
	password	varchar(100) NOT NULL,
	ruolo		role,
PRIMARY KEY (codfiscale)
);

CREATE TABLE Edifici(
	codedificio varchar(50) NOT NULL,
	indirizzo varchar(255) NOT NULL,
	PRIMARY KEY(codedificio)
	);

CREATE TABLE Aule(
	codaula int NOT NULL,
	capienza int NOT NULL,
	edificio varchar(50) NOT NULL,
	piano int NOT NULL,
	PRIMARY KEY(codaula),
	FOREIGN KEY(edificio) REFERENCES Edifici(codedificio)
	);



CREATE TABLE Corsi(
	codcorso varchar(50) NOT NULL,
	nome 			varchar(100) NOT NULL,
	professore		varchar(100) NOT NULL,
	datainizio          date NOT NULL,
	datafine            date NOT NULL,
	descrizione		varchar(255)	,
	CHECK (datafine > datainizio),
PRIMARY KEY (codcorso),
FOREIGN KEY (professore) REFERENCES Utenti(codfiscale)
);


CREATE TABLE Iscrizioni_corsi(
	corso varchar(50) NOT NULL,
	studente varchar(50) NOT NULL,
	PRIMARY KEY (corso,studente),
	FOREIGN KEY (studente) REFERENCES Utenti(codfiscale),
	FOREIGN KEY (corso) REFERENCES Corsi(codcorso)
);


CREATE TABLE Prenotazioni_lezioni(
	codprenotazione SERIAL 	NOT NULL,
	corso 		varchar(50) NOT NULL,
	aula int ,
	datainizio  timestamp NOT NULL,
	durata    timestamp  NOT NULL,
	maxpresenti int,
	online boolean,
	CHECK (durata > datainizio),
	CHECK (online AND maxpresenti = 0 OR online != True AND maxpresenti > 0 ),
PRIMARY KEY (codprenotazione),
FOREIGN KEY (corso) REFERENCES Corsi(codcorso),
FOREIGN KEY (aula) REFERENCES Aule(codaula)
);

CREATE TABLE Prenotazioni_posti(
	utente varchar(100) NOT NULL,
	lezione int NOT NULL,


PRIMARY KEY (utente, lezione),
FOREIGN KEY (utente) REFERENCES Utenti(codfiscale),
FOREIGN KEY (lezione) REFERENCES Prenotazioni_lezioni(codprenotazione)
);


/*trigger*/


CREATE OR REPLACE FUNCTION disponibilita_lez()
RETURNS TRIGGER AS $$
BEGIN
	if NEW.aula IN (SELECT pl.aula
				   FROM Prenotazioni_lezioni pl
				   WHERE (NEW.durata >= pl.datainizio AND NEW.datainizio <= pl.durata)) THEN
		RETURN NULL;
		
	END IF;
	
	RETURN NEW;
	
	
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION checkprof()
RETURNS TRIGGER AS $$
BEGIN
	if NEW.professore IN (SELECT u.codfiscale
				   FROM Utenti u
				   WHERE u.ruolo = 'professore') THEN
		RETURN NEW;
		
	END IF;
	
	RETURN NULL;
	
	
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION capienza_max()
RETURNS TRIGGER AS $$
BEGIN
	if NEW.maxpresenti > (SELECT a.capienza
							FROM Aule a
							WHERE a.codaula = NEW.aula ) THEN

		RETURN NULL;
		
	END IF;
	
	RETURN NEW;
	
	
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER corsoprof
BEFORE INSERT OR UPDATE ON Corsi
FOR EACH ROW EXECUTE PROCEDURE  checkprof();

CREATE TRIGGER disponibilita_aula
BEFORE INSERT OR UPDATE ON Prenotazioni_lezioni
FOR EACH ROW EXECUTE PROCEDURE  disponibilita_lez();

CREATE TRIGGER posti_aule_prenotazioni
BEFORE INSERT OR UPDATE ON Prenotazioni_lezioni
FOR EACH ROW EXECUTE PROCEDURE  capienza_max();
