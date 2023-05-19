DROP TABLE IF EXISTS adminUser;
DROP TABLE IF EXISTS besvarelse;
DROP TABLE IF EXISTS brukere;
DROP TABLE IF EXISTS fasitsvar;
DROP TABLE IF EXISTS spørsmålsbank;
DROP TABLE IF EXISTS quizOversikt;

-- -----------------------------------------------------
-- quizOversikt
-- -----------------------------------------------------
CREATE TABLE quizOversikt (
  `quizId` INT(11) NOT NULL AUTO_INCREMENT,
  `tittel` VARCHAR(50) NULL DEFAULT NULL,
  `antallSpørsmål` INT(11) NULL DEFAULT NULL,
  `aktiv` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (quizId),
  CONSTRAINT uniktittel UNIQUE (`tittel`));

INSERT INTO quizOversikt (`tittel`, `antallSpørsmål`, `aktiv`)
VALUES ("Test din kunnskap om elefanter", 5, 1),
		("Norge", 10, 1),
    ("Hvor mye arbeid er lagt i dette prosjektet", 6, 1);
        
        
-- -----------------------------------------------------
-- spørsmålsbank
-- -----------------------------------------------------
CREATE TABLE spørsmålsbank (
  `spørsmålId` INT AUTO_INCREMENT,
  `spørsmål` VARCHAR(200) NULL DEFAULT NULL,
  `spørsmålstype` VARCHAR(50) NULL DEFAULT NULL,
  `quizId` INT(11) NOT NULL,
  `aktiv` BOOLEAN NOT NULL DEFAULT TRUE,
  `kategori` VARCHAR(200) NOT NULL DEFAULT "ukategorisert",
  PRIMARY KEY (`spørsmålId`),
  FOREIGN KEY (quizId) REFERENCES quizOversikt(quizId));

    
INSERT INTO spørsmålsbank(`spørsmål`, `spørsmålstype`, `quizId`, `kategori`)
VALUES ("Hvor gammel er den eldste dokumenterte elefanten?", "enkeltvalgs", 1, "dyr"),
		("Hva heter babyen til elefanten?", "enkeltvalgs", 1, "dyr"),
        ("Hva slags dyr er elefanten?", "enkeltvalgs", 1, "dyr"),
        ("Hvilken farge er  elefantens hud?", "enkeltvalgs", 1, "dyr"),
        ("Hører elefanter hjemme i sirkus?", "enkeltvalgs", 1, "dyr"),
        
        ("Hvor mange byer er det ikke i Norge?", "flervalgs", 2, "geografi"),
        ("Hva heter Norges to største byer?", "flervalgs", 2, "geografi"),
        ("Hva heter Norges to minste byer?", "flervalgs", 2, "geografi"),
        ("Velg tidligere statsministre i Norge", "flervalgs", 2, "geografi"),
        ("Velg severdighetene i Norge", "flervalgs", 2, "geografi"),
        ("Hvilken to byer er nærmest hovedstaten?", "flervalgs", 2, "geografi"),
        ("Hvilket land har Norge vært en del av?", "flervalgs", 2, "geografi"),
        ("Hvilke dyr er vanligst å ha i Norge?", "flervalgs", 2, "geografi"),
        ("Hvilken bokstaver har det norske alfabetet som det engelske ikke har?", "flervalgs", 2, "geografi"),
        ("Hvilken av byene nedenfor er ikke en norsk by?", "flervalgs", 2, "geografi"),

        ("Hvor mange timer har Jan-Cato brukt på å fikse opp etter Chris i style.css?", "enkeltvalgs", 3, "Oblig 3"),
        ("Har Beyan plagdes med kobling mellom webapp og html?", "enkeltvalgs", 3, "Oblig 3"),
        ("Hvor mange linjer med kode tror du ca. vi har skrevet i dette prosjektet?", "enkeltvalgs", 3, "Oblig 3"),
        ("Hvor mange kopper med kaffe tror du vi har drukket mens vi jobbet med dette prosjektet?", "enkeltvalgs", 3, "Oblig 3"),
        ("Hvor mange utkommenterte linjer har vi slettet for å gjøre koden fin??", "enkeltvalgs", 3, "Oblig 3"),
        ("Hvem føler at dem har lært mye av denne oppgaven så langt?", "flervalgs", 3, "Oblig 3");
        
    

-- -----------------------------------------------------
-- svar
-- -----------------------------------------------------
CREATE TABLE `fasitsvar` (
  `svarId` INT NULL DEFAULT NULL AUTO_INCREMENT,
  `spørsmålId` INT,
  `svaralternativ` VARCHAR(200),
  `riktigGalt` BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (svarId, svaralternativ),
  FOREIGN KEY(spørsmålId) REFERENCES spørsmålsbank(spørsmålId));
  

INSERT INTO fasitsvar(`spørsmålId`, `svaralternativ`, `riktigGalt`)
VALUES
	(1, "89", 1),
    (1, "100", 0),
    (1, "78", 0),
    (2, "elli", 0),
    (2, "fantorangen", 0),
    (2, "kalv", 1),
    (3, "pattedyr", 1),
    (3, "virveldyr", 0),
    (3, "store dyr", 0),
    (4, "grå", 1),
    (4, "blå", 0),
    (4, "rosa", 0),
    (5, "ja", 0),
    (5, "nei", 0),
    (5, "usikker", 0),
    
    (6, "108", 0),
    (6, "99", 1),
    (6, "102", 1),
    (7, "Oslo", 1),
    (7, "Bergen", 1),
    (7, "Stavanger", 0),
    (8, "Kolvereid", 1),
    (8, "Tvedestrand", 1),
    (8, "Mandal", 0),
    (9, "Erna Solberg", 1),
    (9, "Jens Stoltenberg", 1),
    (9, "Jon Almaas", 0),
    (10, "sinnataggen", 1),
    (10, "operaen", 1),
    (10, "gulvet på rema 1000", 0),
    (11, "Sjølyststranda", 1),
    (11, "Nesoddtangen", 1), 
    (11, "Kolbotn", 0),
    (12, "Sverige", 1),
    (12, "Danmark", 1),
    (12, "Kosovo", 0),
    (13, "katt", 1),
    (13, "hund", 1),
    (13, "hamster", 0),
    (14, "Æ", 1),
    (14, "Å", 1),
    (14, "A", 0),
    (15, "Stockholm", 1),
    (15, "Paris", 1),
    (15, "Oslo", 0),

    (16,"2", 0),
    (16,"6", 0),
    (16,"12. Chris er foresten bannlyst fra CSS", 1),
    (17,"Ja", 0),
    (17,"Nei", 0),
    (17,"Chris til unnsetning", 1),
    (18,"1500", 0),
    (18,"For mange", 1),
    (18,"2000", 0),
    (19,"har ikke gått i kopper, men flere kanner per dag!", 1),
    (19,"20", 0),
    (19,"40", 0),
    (20,"300", 0),
    (20,"600", 0),
    (20,"3 ganger så mange linjer kode enn det som prosjektet består av per dags dato", 1),
    (21,"Beyan", 1),
    (21,"Chris", 1),
    (21,"Jan-Cato", 1);


CREATE TABLE brukere(
`id` INT AUTO_INCREMENT PRIMARY KEY,
`brukernavn` VARCHAR(45),
`quizId` INT(11) NOT NULL, 
FOREIGN KEY (quizId) REFERENCES quizOversikt(quizId));

INSERT INTO brukere(`brukernavn`, `quizId`)
VALUES ("Cato", 1),
		("beyan", 1),
        ("Chris", 1);


CREATE TABLE besvarelse(
`id` INT,
`svarId` INT(11),
`brukersvar` BOOLEAN NOT NULL DEFAULT FALSE, 
PRIMARY KEY(id, svarId),
FOREIGN KEY(id) REFERENCES brukere(id),
FOREIGN KEY(svarId) REFERENCES fasitsvar(svarId));

INSERT INTO besvarelse(`id`, `svarId`, `brukersvar`)
VALUES (1, 1, 0),
		(1, 2, 0),
        (1, 3, 1),
        (1, 4, 1),
        (1, 5, 0),
        (1, 6, 0),
        (1, 7, 1),
        (1, 8, 0),
        (1, 9, 0),
        (1, 10, 0),
        (1, 11, 0),
        (1, 12, 1),
        (1, 13, 0),
        (1, 14, 0),
        (1, 15, 1),
        (1, 16, 1),
        (1, 17, 0),
        (1, 18, 0),
        (2, 1, 1),
        (2, 2, 0),
        (2, 3, 0),
        (3, 1, 1),
        (3, 2, 0),
        (3, 3, 0);
        
-- -----------------------------------------------------
-- admin
-- -----------------------------------------------------
CREATE TABLE adminUser (
  `adminId` INT(11) NOT NULL AUTO_INCREMENT,
  `brukernavn` VARCHAR(50) NOT NULL DEFAULT "",
  `fornavn` VARCHAR(50) NOT NULL DEFAULT "",
  `etternavn` VARCHAR(50) NOT NULL DEFAULT "",
  `passord` VARCHAR(50) NOT NULL DEFAULT "123456",
  PRIMARY KEY (adminId),
  CONSTRAINT uniktittel UNIQUE (`brukernavn`));

INSERT INTO adminUser (`brukernavn`, `fornavn`, `etternavn`, `passord`)
VALUES ("knut", "Knut", "Knutsen", "4152"),
		("jens", "Donald", "Duck","123");