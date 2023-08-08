INSERT INTO Utenti VALUES ('admin', 'admin','admin',25,0,'0','admin','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','admin');
INSERT INTO Utenti VALUES ('codMario', 'mario','rossi',26,0,'0','emailMario','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');
INSERT INTO Utenti VALUES ('codMaria', 'maria','rossi',35,1,'0','emailMaria','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');

INSERT INTO Utenti (codFiscale, nome, cognome, eta, sesso, cellulare, email, password, ruolo)
VALUES
    ('CF001', 'Mario', 'Rossi', 25, 1, '+123456789', 'mario@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'utente'),
    ('CF002', 'Laura', 'Bianchi', 22, 0, '+987654321', 'laura@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'utente'),
    ('CF003', 'Luigi', 'Verdi', 28, 1, '+555555555', 'luigi@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'professore'),
    ('CF004', 'Anna', 'Gialli', 20, 0, '+111111111', 'anna@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'utente'),
    ('CF005', 'Roberto', 'Neri', 30, 1, '+999999999', 'roberto@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'admin');

-- Inserimento di esami di prova
INSERT INTO Esami (codEsame, materia, docenteReferente, docente)
VALUES
    ('E001', 'Matematica', 'CF003', NULL),
    ('E002', 'Fisica', 'CF003', NULL),
    ('E003', 'Informatica', 'CF003', NULL);

-- Inserimento di esami superati di prova
INSERT INTO Esami_superati (esame, studente, voto)
VALUES
    ('E001', 'CF001', 28),
    ('E001', 'CF002', 25),
    ('E002', 'CF001', 30),
    ('E002', 'CF002', 27);
    
-- Inserimento di prove di prova
INSERT INTO Prove (codProva, nomeProva, esame, docenteReferente, tipoProva, dataProva, dataScandenza, richestoSuperamentoCodProva, completo)
VALUES
    ('P001', 'Parziale', 'E001', 'CF003', 'voto', '2023-08-01 10:00:00', '2023-08-01 12:00:00', NULL, true),
    ('P002', 'Finale', 'E001', 'CF003', 'voto', '2023-08-15 14:00:00', '2023-08-15 16:00:00', 'P001', false),
    ('P003', 'Pratica', 'E002', 'CF003', 'voto', '2023-08-10 11:00:00', '2023-08-10 13:00:00', NULL, true);

-- Inserimento di risultati delle prove
INSERT INTO Risulato_prove (prova, voto, studente)
VALUES
    ('P001', 'voto', 'CF001'),
    ('P002', 'voto', 'CF002'),
    ('P003', 'voto', 'CF003');


-- Inserimento di iscrizioni a prove di prova
INSERT INTO Iscrizione_prove (risultato, prova, studente)
VALUES
    (NULL, 'P001', 'CF001'),
    (NULL, 'P002', 'CF002'),
    (NULL, 'P003', 'CF003');