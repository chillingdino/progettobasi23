INSERT INTO Utenti VALUES ('admin', 'admin','admin',25,0,'0','admin','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','admin');
INSERT INTO Utenti VALUES ('codMario', 'mario','rossi',26,0,'0','emailMario','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');
INSERT INTO Utenti VALUES ('codMaria', 'maria','rossi',35,1,'0','emailMaria','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','utente');

INSERT INTO Utenti VALUES ('codCALZAVARA', 'Stefano','CALZAVARA',25,0,'0','emailCALZAVARA','$2b$10$aTaqNiv5vBc1SdkscE0TT.cKk9/sQESmt/W2PoZ8vREQ501aA8DiG','professore');

INSERT INTO Edifici VALUES ('zeta1', 'viatorino48947');
INSERT INTO Edifici VALUES ('alfa', 'viatorino48947');
INSERT INTO Edifici VALUES ('beta', 'viatorino48947');
INSERT INTO Edifici VALUES ('gamma', 'viatorino48947');

INSERT INTO Aule VALUES (1, 100, 'zeta1', 2);

INSERT INTO Corsi VALUES ('stat22','statistica2022','codCALZAVARA','2022-01-01 08:00:00', '2022-05-01 08:00:00', 'Corso di statistica 2022');
INSERT INTO Corsi VALUES ('java1','java','codCALZAVARA','2022-01-01 00:00:00', '2022-06-01 00:00:00', 'Corso di programmazione ad oggetti');

INSERT INTO Iscrizioni_corsi VALUES('stat22', 'codMario');
INSERT INTO Iscrizioni_corsi VALUES('stat22', 'codMaria');

INSERT INTO Iscrizioni_corsi VALUES('java1', 'codMario');