INSERT INTO Utenti VALUES ('admin', 'admin','admin',25,0,'0','admin','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','admin');
INSERT INTO Utenti VALUES ('codMario', 'mario','rossi',26,0,'0','emailMario','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');

INSERT INTO Utenti (codFiscale, nome, cognome, eta, sesso, cellulare, email, password, ruolo)
VALUES
    ('CF001', 'Mario', 'Rossi', 25, 1, '+123456789', 'mario@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'utente'),
    ('CF002', 'Laura', 'Bianchi', 22, 0, '+987654321', 'laura@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'utente'),
    ('CF003', 'Luigi', 'Verdi', 28, 1, '+555555555', 'luigi@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'professore'),
    ('CF004', 'Marco', 'Rossi', 28, 1, '+555555555', 'marco@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'professore'),
    ('CF005', 'Anna', 'Gialli', 20, 0, '+111111111', 'anna@email.com', '$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG', 'utente'),
    

-- Inserimento di esami di prova
INSERT INTO Esami (codEsame, materia, docenteReferente, docente)
VALUES
    ('E001', 'Matematica', 'CF003', NULL),
    ('E002', 'Fisica', 'CF003', NULL),
    ('E003', 'Informatica', 'CF003', NULL);

-- Popolare la tabella Prove con dati di esempio
INSERT INTO Prove (codProva, nomeProva, esame, docenteReferente, descrizione, durata, tipoProva, dataProva, dataScandenza, richestoSuperamentoCodProva, completo)
VALUES
    ('P001', 'Esame Finale', 'E001', 'CF003', 'Esame finale di Matematica', '3 ore', 'voto', '2023-09-30 10:00:00', '2023-09-30 13:00:00', NULL, true),
    ('P002', 'Esame Parziale', 'E002', 'CF004', 'Esame parziale di Fisica', '2 ore', 'voto', '2023-09-22 14:00:00', '2023-09-22 16:00:00', NULL, false);
    ('P003', 'Esame Finale', 'E002', 'CF004', 'Esame parziale di Fisica', '2 ore', 'voto', '2023-09-22 14:00:00', '2023-09-22 16:00:00', P2, true);

-- Inserimento di esami superati di prova
INSERT INTO Esami_superati (esame, studente, voto)
VALUES
    ('E001', 'CF001', 28),
    ('E001', 'CF002', 25),
    ('E001', 'CF001', 30),
    ('E001', 'CF002', 27);

-- Inserimento di risultati delle prove
INSERT INTO Risulato_prove (prova, voto, studente)
VALUES
    ('P002', '10', 'CF001'),
    ('P002', '30', 'CF002'),
    ('P002', '20', 'CF003');

-- Inserimento di iscrizioni a prove di prova
INSERT INTO Iscrizione_prove (prova, studente)
VALUES
    ('P001', 'CF001'),
    ('P002', 'CF002'),
    ( 'P003', 'CF003');