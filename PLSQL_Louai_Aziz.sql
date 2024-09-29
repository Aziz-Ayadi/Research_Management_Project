-- --------------------------------------------- Question 1 & 2 -----------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------
Create Table Faculte (
	facno Int Not Null,
	facnom Varchar(10),
	adresse Varchar(20), 
	libelle Varchar(50), 
	Primary Key (facno)
);

Insert Into Faculte Values (1, 'FST', 'Manar 2', 'Faculté des sciences de Tunis');
Insert Into Faculte Values (2, 'ENIT', 'Manar 2', 'Ecole nationale des ingénieurs de Tunis');
Insert Into Faculte Values (3, 'ENIC', 'Carthage', 'Ecole nationale des ingénieurs de Carthage');

select * from faculte ;

-- *********************************************************************************************************

Create Table Laboratoire ( 
	labno Int Not Null,
	labnom Varchar(30),
	facno Int,
	Primary Key (labno),
	Foreign Key (facno) References Faculte (facno) 
);

Insert Into laboratoire Values (1, 'Lab info', 2); 
Insert Into laboratoire Values (2, 'Lab maths', 2);
Insert Into laboratoire Values (3, 'Lab info', 3);
Insert Into laboratoire Values (4, 'Lab maths', 3); 
Insert Into laboratoire Values (5,  'Lab écologique', 1); 
Insert Into laboratoire Values (6, 'Lab médicale', 1);
Insert Into laboratoire Values (7, 'Lab politique', 1);

Select * From laboratoire;

-- *********************************************************************************************************

Create Table Chercheur ( 
	chno Int Not Null,
	chnom Varchar(30), 
	grade Varchar(2), 
	statut Varchar(1), 
	daterecrut date, 
	salaire NUMERIC(8,3),
	prime NUMERIC(8,3), 
	email Varchar(30),
	supno int,
	labno int,
	facno int,
	Primary Key (chno),
	Foreign Key (supno) References Chercheur (chno),
	Foreign Key (labno) References Laboratoire (labno), 
	Foreign Key (facno) References Faculte (facno)
);

Insert Into Chercheur Values (7, 'Mohamed', 'PR', 'P', '02-01-2023', 2500, 200, 'mohamed@gmail.com', Null, 3, 3);
Insert Into Chercheur Values (6, 'Achref', 'PR', 'P', '01-01-2023', 2500, 200, 'achref@gmail.com', Null, 1, 2); 
Insert Into Chercheur Values (1, 'Aziz', 'E', 'C', '28-06-2023', 1700, 200, 'aziz@gmail.com', 6, 1, 2); 
Insert Into Chercheur Values (2, 'Louai', 'D', 'C', '28-02-2023', 1500, 200, 'louai@gmail.com', 6, 1, 2); 
Insert Into Chercheur Values (3, 'Rayen', 'A', 'C', '10-03-2023', 1800, 500, 'rayen@gmail.com', 7, 3, 3); 
Insert Into Chercheur Values (4, 'Bilel', 'MA', 'P', '23-04-2023', 1800, 400, 'bilel@gmail.com', 7, 3, 3); 
Insert Into Chercheur Values (5, 'Sami', 'MC', 'P', '24-05-2023', 2000, 300, 'sami@gmail.com', 6, 1, 2); 
							  
Select * From Chercheur;
						 
-- *********************************************************************************************************

Create Table Publication (
	pubno Varchar(7) Not Null,
	titre Varchar(20),
	theme Varchar(15),
	type_p Varchar(2),
	volume_p int,
	date_p date,
	apparition Varchar(20),
	Editeur Varchar(20),
	Primary Key (pubno)
);

Insert Into Publication Values ('23-0001', 'AI et data science', 'Informatique', 'AS', 300, '01-12-2023', 'conférence de AI', 'Axel Wietsel'); 
Insert Into Publication Values ('23-0002', 'Le cancer', 'Médicale', 'PC', 150, '24-08-2023', 'Jour de cancer', 'Lewandowski'); 
Insert Into Publication Values ('23-0003', 'La robotique', 'Informatique', 'P', 5, '09-10-2023', 'La technologie', 'Jerome Boateng'); 
Insert Into Publication Values ('23-0004', 'Equation diff', 'Mathematiques', 'L', 100, '15-03-2023', 'conférence de maths', 'Pedri'); 
Insert Into Publication Values ('23-0005', 'La pollution', 'Ecologique', 'T', 200, '05-01-2023', 'Soutenance', 'Van De Ven'); 
Insert Into Publication Values ('23-0006', 'Palestine', 'Politique', 'M', 500, '04-04-2023', 'Soutenance', 'Mitoma');

Select * From publication;

-- *********************************************************************************************************

Create Table Publier ( 
	chno int Not Null,
	pubno Varchar(7) Not Null,
	rang int,
	Primary Key (chno, pubno),
	Foreign Key (chno) References Chercheur (chno),
	Foreign Key (pubno) References Publication (pubno)
);

Insert Into Publier Values (1, '23-0001', 1);
Insert Into Publier Values (2, '23-0001', 2);
Insert Into Publier Values (3, '23-0003', 1);
Insert Into Publier Values (4, '23-0003', 2);
Insert Into Publier Values (5, '23-0001', 1);
Insert Into Publier Values (2, '23-0002', 1); 
Insert Into Publier Values (4, '23-0004', 1);

Select * From Publier;

-- --------------------------------------------- Question 4 ---------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------

Create Table historique_chercheurs (
            chno int,
            chnom varchar2(30),
            grade varchar2(2),
            statut varchar2(1),
            daterecrut date,
            salaire int,
            prime int,
            email varchar2(30),
            supno int,
            labno int,
            facno int,
            action_effectuee varchar2(20),
            Primary Key (chno),
            Foreign Key (supno) References chercheur (chno),
            Foreign Key (labno) References laboratoire (labno),
            Foreign Key (facno) References Faculte (facno)
    );

CREATE OR REPLACE TRIGGER historique_chercheurs
BEFORE UPDATE OR DELETE ON chercheur
FOR EACH ROW
DECLARE
    -- Variables pour stocker les informations du chercheur avant la modification ou suppression
    v_chno_origine chercheur.chno%TYPE;
    v_chnom_origine chercheur.chnom%TYPE;
    v_grade_origine chercheur.grade%TYPE;
    v_statut_origine chercheur.statut%TYPE;
    v_daterecrut_origine chercheur.daterecrut%TYPE;
    v_salaire_origine chercheur.salaire%TYPE;
    v_prime_origine chercheur.prime%TYPE;
    v_email_origine chercheur.email%TYPE;
    v_supno_origine chercheur.supno%TYPE;
    v_labno_origine chercheur.labno%TYPE;
    v_facno_origine chercheur.facno%TYPE;

BEGIN
    -- Stocker les informations du chercheur avant la modification ou suppression
    v_chno_origine := :OLD.chno;
    v_chnom_origine := :OLD.chnom;
    v_grade_origine := :OLD.grade;
    v_statut_origine := :OLD.statut;
    v_daterecrut_origine := :OLD.daterecrut;
    v_salaire_origine := :OLD.salaire;
    v_prime_origine := :OLD.prime;
    v_email_origine := :OLD.email;
    v_supno_origine := :OLD.supno;
    v_labno_origine := :OLD.labno;
    v_facno_origine := :OLD.facno;


    -- Insérer les informations dans la table historique_chercheurs
    IF UPDATING THEN
        INSERT INTO historique_chercheurs (
            chno,
            chnom,
            grade,
            statut,
            daterecrut,
            salaire,
            prime,
            email,
            supno,
            labno,
            facno,
            action_effectuee
        ) VALUES (
            v_chno_origine,
            v_chnom_origine,
            v_grade_origine,
            v_statut_origine,
            v_daterecrut_origine,
            v_salaire_origine,
            v_prime_origine,
            v_email_origine,
            v_supno_origine,
            v_labno_origine,
            v_facno_origine,
            'Modification'
        );
    ELSIF DELETING THEN
        INSERT INTO historique_chercheurs (
            chno,
            chnom,
            grade,
            statut,
            daterecrut,
            salaire,
            prime,
            email,
            supno,
            labno,
            facno,
            action_effectuee
        ) VALUES (
            v_chno_origine,
            v_chnom_origine,
            v_grade_origine,
            v_statut_origine,
            v_daterecrut_origine,
            v_salaire_origine,
            v_prime_origine,
            v_email_origine,
            v_supno_origine,
            v_labno_origine,
            v_facno_origine,
            'Suppression'
        );
    END IF;
END;
/

Update chercheur Set salaire = 2550 Where chno=1;
select * From historique_chercheurs;
select * From chercheur;
-- *********************************************************************************************************

CREATE OR REPLACE TRIGGER capacite_encadrement
BEFORE INSERT OR UPDATE ON chercheur
FOR EACH ROW
DECLARE
    nb_etudiants NUMBER;
    nb_doctorants NUMBER;
BEGIN
    -- Vérifier uniquement pour les chercheurs de grade E ou D
    IF :NEW.grade IN ('E', 'D') THEN
        -- Calculer le nombre actuel d'étudiants et de doctorants encadrés par le directeur
        SELECT COUNT(*) INTO nb_etudiants
        FROM chercheur
        WHERE supno = :NEW.chno
        AND grade = 'E';

        SELECT COUNT(*) INTO nb_doctorants
        FROM chercheur
        WHERE supno = :NEW.chno
        AND grade = 'D';

        -- Vérifier la capacité d'encadrement
        IF nb_etudiants >= 30 AND :NEW.grade = 'E' THEN
            RAISE_APPLICATION_ERROR(-20001, 'Le directeur a atteint sa capacité maximale d encadrement d étudiants de 3ème cycle.');
        ELSIF nb_doctorants >= 20 AND :NEW.grade = 'D' THEN
            RAISE_APPLICATION_ERROR(-20001, 'Le directeur a atteint sa capacité maximale d encadrement de doctorants.');
        END IF;
    END IF;
END;
/

-- *********************************************************************************************************

CREATE OR REPLACE TRIGGER diminution_salaire
BEFORE UPDATE ON chercheur
FOR EACH ROW
BEGIN
    -- Vérifier si le salaire est en train de diminuer
    IF :NEW.salaire < :OLD.salaire THEN
        -- Empêcher la mise à jour et lever une erreur
        RAISE_APPLICATION_ERROR(-20001, 'La diminution du salaire est interdite.');
    END IF;
END;
/

update chercheur set salaire=1700 where chno=1;

-- *********************************************************************************************************

CREATE OR REPLACE TRIGGER restrictions_temps
BEFORE UPDATE ON chercheur  /* SCHEMA.TABLE1, ... */
FOR EACH ROW  /* STATEMENT */
DECLARE
    jour_semaine VARCHAR2(10);
    heure INT;
BEGIN
    -- Récupérer le jour de la semaine en anglais (e.g., 'MONDAY')
    SELECT TO_CHAR(SYSDATE, 'DAY') INTO jour_semaine FROM DUAL;
    SELECT TO_NUMBER(TO_CHAR(SYSDATE, 'HH24')) INTO heure FROM DUAL;

    -- Vérifier si le jour est un jour ouvrable et l'heure est entre 8h et 18h
    IF (jour_semaine NOT IN ('SAMEDI', 'DIMANCHE') AND heure BETWEEN 8 AND 18) THEN
        -- Continuer la mise à jour
        NULL;
    ELSE
        -- Annuler la mise à jour en levant une erreur
        RAISE_APPLICATION_ERROR(-20001, 'Les mises à jour ne sont autorisées que les jours ouvrables entre 8h et 18h.');
    END IF;
END;
/


-- --------------------------------------------- Question 5 ---------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE ajouter_chercheur(
    p_chno INT,p_chnom VARCHAR(30),p_grade VARCHAR(2),p_statut VARCHAR(1),p_daterecrut DATE,
	p_salaire NUMERIC(8,3),p_prime NUMERIC(8,3),p_email VARCHAR(30),p_supno INT,p_labno INT,p_facno INT
)
AS $$
BEGIN

	IF EXISTS (SELECT 1 FROM Chercheur WHERE chno = p_chno) THEN
        RAISE EXCEPTION 'Le chercheur avec le numéro % existe déjà.', p_chno;
    END IF;

    IF p_grade NOT IN ('E', 'D', 'A', 'MA', 'MC', 'PR') THEN
        RAISE EXCEPTION 'Grade invalide : %.', p_grade;
    END IF;

    IF p_statut NOT IN ('P', 'C') THEN
        RAISE EXCEPTION 'Statut invalide : %.', p_statut;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM Laboratoire WHERE labno = p_labno) THEN
        RAISE EXCEPTION 'Le laboratoire avec le numéro % n''existe pas.', p_labno;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM Faculte WHERE facno = p_facno) THEN
        RAISE EXCEPTION 'La faculté avec le numéro % n''existe pas.', p_facno;
    END IF;

    INSERT INTO Chercheur (
        chno, chnom, grade, statut, daterecrut,
        salaire, prime, email, supno, labno, facno
    ) VALUES (
        p_chno, p_chnom, p_grade, p_statut, p_daterecrut,
        p_salaire, p_prime, p_email, p_supno, p_labno, p_facno
    );
--     COMMIT;
END;
$$ LANGUAGE plpgsql;


CALL ajouter_chercheur(
    8, 'Oubaida', 'PR', 'P', '2023-10-07', 5000, 1000,
    'oubaida@email.com', NULL, 1, 1
);
Select * From Chercheur ;
where chno = 8;

-- *********************************************************************************************************
CREATE OR REPLACE PROCEDURE modifier_profil_chercheur(
    p_chno INT,p_chnom VARCHAR(30) DEFAULT NULL,p_grade VARCHAR(2) DEFAULT NULL,p_statut VARCHAR(1) DEFAULT NULL,
	p_daterecrut DATE DEFAULT NULL,p_salaire NUMERIC(8,3) DEFAULT NULL,p_prime NUMERIC(8,3) DEFAULT NULL,
	p_email VARCHAR(30) DEFAULT NULL,p_supno INT DEFAULT NULL,p_labno INT DEFAULT NULL,p_facno INT DEFAULT NULL
)
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Chercheur WHERE chno = p_chno) THEN
        RAISE EXCEPTION 'Le chercheur avec le numéro % n''existe pas.', p_chno;
    END IF;

    IF p_chnom IS NOT NULL THEN
        UPDATE Chercheur SET chnom = p_chnom WHERE chno = p_chno;
    END IF;

    IF p_grade IS NOT NULL THEN
        IF p_grade NOT IN ('E', 'D', 'A', 'MA', 'MC', 'PR') THEN
            RAISE EXCEPTION 'Grade invalide : %.', p_grade;
        END IF;
        UPDATE Chercheur SET grade = p_grade WHERE chno = p_chno;
    END IF;

    IF p_statut IS NOT NULL THEN
        IF p_statut NOT IN ('P', 'C') THEN
            RAISE EXCEPTION 'Statut invalide : %.', p_statut;
        END IF;
        UPDATE Chercheur SET statut = p_statut WHERE chno = p_chno;
    END IF;

    IF p_daterecrut IS NOT NULL THEN
        UPDATE Chercheur SET daterecrut = p_daterecrut WHERE chno = p_chno;
    END IF;

    IF p_salaire IS NOT NULL THEN
        UPDATE Chercheur SET salaire = p_salaire WHERE chno = p_chno;
    END IF;

    IF p_prime IS NOT NULL THEN
        UPDATE Chercheur SET prime = p_prime WHERE chno = p_chno;
    END IF;

    IF p_email IS NOT NULL THEN
        UPDATE Chercheur SET email = p_email WHERE chno = p_chno;
    END IF;

    IF p_supno IS NOT NULL THEN
        UPDATE Chercheur SET supno = p_supno WHERE chno = p_chno;
    END IF;

    IF p_labno IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM Laboratoire WHERE labno = p_labno) THEN
            RAISE EXCEPTION 'Le laboratoire avec le numéro % n''existe pas.', p_labno;
        END IF;
        UPDATE Chercheur SET labno = p_labno WHERE chno = p_chno;
    END IF;

    IF p_facno IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM Faculte WHERE facno = p_facno) THEN
            RAISE EXCEPTION 'La faculté avec le numéro % n''existe pas.', p_facno;
        END IF;
        UPDATE Chercheur SET facno = p_facno WHERE chno = p_chno;
    END IF;

END;
$$ LANGUAGE plpgsql;


CALL modifier_profil_chercheur(8, 'Abou Oubaida', NULL , 'C', NULL, 5500, NULL, NULL, NULL	, NULL, NULL);
Select * From Chercheur 
where chno = 8;

-- *********************************************************************************************************

select * from publication ;

CREATE OR REPLACE FUNCTION chercheurs_lab_plus_publications(
    p_date_debut DATE,
    p_date_fin DATE
)
RETURNS TABLE (
    facnom VARCHAR(30),
    labnom VARCHAR(30),
    chno INT,
    chnom VARCHAR(30),
    nb_publications BIGINT  
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        f.facnom,
        l.labnom,
        c.chno,
        c.chnom,
        COUNT(p.pubno) AS nb_publications
    FROM
        Faculte f
        JOIN Laboratoire l ON f.facno = l.facno
        JOIN Chercheur c ON l.labno = c.labno
        LEFT JOIN Publier pub ON c.chno = pub.chno
        LEFT JOIN Publication p ON pub.pubno = p.pubno
    WHERE
        p.date_p BETWEEN p_date_debut AND p_date_fin
    GROUP BY
        f.facnom, l.labnom, c.chno, c.chnom
    ORDER BY
        nb_publications DESC ;

    RETURN;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM chercheurs_lab_plus_publications('2023-01-01', '2023-12-31');

-- *********************************************************************************************************

CREATE OR REPLACE PROCEDURE supprimer_chercheur(
    p_chno INT
)
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Chercheur WHERE chno = p_chno) THEN
        RAISE EXCEPTION 'Le chercheur avec le numéro % n''existe pas.', p_chno;
    END IF;

    UPDATE Chercheur SET supno = NULL WHERE supno = p_chno;

    DELETE FROM Publier WHERE chno = p_chno;

    DELETE FROM Chercheur WHERE chno = p_chno;

--     COMMIT;
END;
$$ LANGUAGE plpgsql;

CALL supprimer_chercheur(7);
select * from chercheur ;














