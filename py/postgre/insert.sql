-- Insert data into the Utenti table
INSERT INTO Utenti VALUES ('admin', 'admin','admin',25,0,'0','admin','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','admin');
INSERT INTO Utenti VALUES ('codMario', 'mario','rossi',26,0,'0','emailMario','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');
INSERT INTO Utenti VALUES ('codMaria', 'maria','rossi',35,1,'0','emailMaria','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');

-- Insert data into the Esami_superati table
INSERT INTO Esami_superati (esame, studente, voto)
VALUES ('Esame1', 'student1', 90),
       ('Esame1', 'student2', 85),
       ('Esame2', 'student2', 92);

-- Insert data into the Prove table
INSERT INTO Prove (codProva, esame, docenteReferente, tipoProva, dataProva, dataScandenza)
VALUES ('Prova1', 'Esame1', 'DocenteReferente1', 'TipoProva1', '2023-07-19 09:00:00', '2023-07-19 12:00:00'),
       ('Prova2', 'Esame1', 'DocenteReferente1', 'TipoProva2', '2023-07-20 14:00:00', '2023-07-20 17:00:00'),
       ('Prova3', 'Esame2', 'DocenteReferente2', 'TipoProva3', '2023-07-21 10:00:00', '2023-07-21 13:00:00');

-- Insert data into the ProvePerEsami table
INSERT INTO ProvePerEsami (esame, prova)
VALUES ('Esame1', 'Prova1'),
       ('Esame1', 'Prova2'),
       ('Esame2', 'Prova3');

-- Insert data into the Iscrizione_prove table
INSERT INTO Iscrizione_prove (risultato, prova, studente)
VALUES (null, 'Prova1', 'student1'),
       (null, 'Prova1', 'student2'),
       (null, 'Prova2', 'student2');