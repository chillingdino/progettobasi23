CREATE TYPE ruolo as ENUM('utente', 'professore', 'admin');
CREATE TYPE valoreProva as ENUM('bonus', 'voto', 'idoneo', 'insuf');

CREATE TABLE Utenti(
 codFiscale varchar(100)  NOT NULL,
 nome  varchar(100) NOT NULL,
 cognome  varchar(100) NOT NULL,
 eta   smallint NOT NULL,
 sesso  smallint NOT NULL,
 cellulare varchar(50),
 email  varchar(100) UNIQUE NOT NULL,
 password varchar(100) NOT NULL,
 ruolo  ruolo,
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

CREATE TABLE Prove(
    codProva varchar(50) not null,
	nomeProva varchar(50) not null,  --rimuovare nome "prova" da qui
  	esame varchar(50) not null,
    docenteReferente varchar(50), -- add not null

    descrizione varchar(50),
    durata varchar(50), --int non varchar, add not null
    
    tipoProva varchar(50), --tipo metterlo con enum
    dataProva timestamp not null, 
    dataScandenza timestamp not null,
	richestoSuperamentoCodProva varchar(50),
	completo boolean not null,
  	PRIMARY KEY (codProva),
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
	nomeProva varchar(50) not null, 
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

CREATE TABLE Esami_superati(
 esame varchar(50) NOT NULL,
 studente varchar(50) NOT NULL,
    voto int not null,
 PRIMARY KEY (esame,studente),
 FOREIGN KEY (studente) REFERENCES Utenti(codFiscale),
 FOREIGN KEY (esame) REFERENCES Esami(codEsame)
);

CREATE TABLE Risulato_prove(
 prova varchar(50) not null,
 voto varchar(50) not null,
 studente varchar(50) not null,
 FOREIGN KEY (prova) REFERENCES Prove(codProva),
 FOREIGN KEY (studente) REFERENCES Utenti(codFiscale)
);

CREATE TABLE Iscrizione_prove(
	risultato int, --perche ce questo boh? 
	prova varchar(50),
	studente varchar(50),
  	PRIMARY KEY (prova,studente),
	FOREIGN KEY (prova) REFERENCES Prove(codProva),
	FOREIGN KEY (studente) REFERENCES Utenti(codFiscale)
);

--trigger che impedisce iscrizione a prova se studente non ha >18 voto su richiestaprova
CREATE TRIGGER prevent_iscrizione_prova_requisiti
BEFORE INSERT ON Iscrizione_prove
FOR EACH ROW
BEGIN
    -- Verifica se richestoSuperamentoCodProva non è NULL
    IF EXISTS (SELECT 1 FROM Prove p WHERE p.codProva = NEW.prova AND p.richestoSuperamentoCodProva IS NOT NULL) THEN
        -- Verifica se lo studente ha un voto > 18 nella prova richiesta
        IF NOT EXISTS (
            SELECT 1
            FROM Risultato_prove rp
            WHERE rp.esame = (
                SELECT richestoSuperamentoCodProva
                FROM Prove
                WHERE codProva = NEW.prova
            ) AND rp.studente = NEW.studente AND rp.voto > 18
        ) THEN
            return null
            SET MESSAGE_TEXT = 'Non è possibile iscriversi alla prova, requisiti non soddisfatti.';
        END IF;
    END IF;
END;


CREATE TRIGGER ControlloCreazioneEsame
BEFORE INSERT ON Prove
FOR EACH ROW
WHEN (NOT EXISTS SELECT * 
		FROM Esami
		WHERE new.prova=Esami.codEsame and (new.docenteReferente=Esami.docente OR new.docenteReferente=Esami.docenteReferente)
BEGIN 
RETURN NULL
END;

--setta a 0 il risultato della prova passata nel caso in cui lo studente si iscriva nuovamente
CREATE TRIGGER invalidaProva
AFTER INSERT ON Iscrizione_prove
FOR EACH ROW
BEGIN
    DECLARE prova_nome VARCHAR(50);
    DECLARE existing_voto INT;

    -- Ottieni il nome della prova per il nuovo record inserito in Iscrizione_prove
    SELECT nomeProva INTO prova_nome
    FROM Prove
    WHERE codProva = NEW.prova;

    -- Controlla se l'utente ha già svolto la prova in passato
    SELECT voto INTO existing_voto
    FROM Risultato_prove rp
    JOIN Prove p ON rp.esame = p.esame
    WHERE p.nomeProva = prova_nome AND rp.studente = NEW.studente;

    -- Se l'utente ha già svolto la prova in passato, imposta a 0 il voto
    IF existing_voto IS NOT NULL THEN
        UPDATE Risultato_prove
        SET voto = 0
        WHERE esame IN (SELECT codEsame FROM Prove WHERE nomeProva = prova_nome) AND studente = NEW.studente;
    END IF;
END;
