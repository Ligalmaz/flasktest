import os
import sqlite3

def f_creerLaBaseDeDonnees():
    if os.path.isfile('base_intervenants.db'):
        print("la base existe déjà.")
    
        liste_intervenants = [
        ('Harris', 'Tote', 'h.tote@hotmail.com'),
        ('Eva', 'Nouie', 'e.nouie@gmail.com'),
        ('Tugudule', 'Niguedouille', 't.niguedouille@wanadoo.fr')]
       
        connexion = sqlite3.connect("base_intervenants.db")
        curseur = connexion.cursor()
        curseur.execute("""
        INSERT INTO intervenants VALUES ('Jean-Lou', 'Le Bars', 'jllebars@gmail.com')
                        """)
        curseur.executemany("INSERT INTO intervenants VALUES(?,?,?)", liste_intervenants)
        connexion.commit()
        connexion.close()
       
    else:
        connexion = sqlite3.connect("base_intervenants.db")
        curseur = connexion.cursor()
        curseur.execute("""
               CREATE TABLE intervenants (
                   prenom_bdd text,
                   nom_bdd text,
                   mail_bdd text
                   )
            """)
        connexion.commit()
        curseur.close()
        connexion.close()

f_creerLaBaseDeDonnees()

# Affichez seulement les personnes qui ont une adresse mail en gmail.
def gmail():
    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.execute(""" SELECT * FROM intervenants WHERE mail_bdd LIKE '%gmail.com%' """)
    print(curseur.fetchall())
    curseur.close()
    connexion.close()


# Modifiez le prénom de M. Le Bars en Jean-Louis.
def jeanlouis():
    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.execute(""" UPDATE intervenants
                        SET prenom_bdd = 'Jean-Louis'
                        WHERE prenom_bdd = 'Jean-Lou' 
                          """)
    connexion.commit()
    print(curseur.fetchall())
    curseur.close()
    connexion.close()
    


# Supprimer les données des personnes qui se prénomment Jean-Louis.
def supprimer_jeanlouis():
    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.execute(""" DELETE FROM intervenants WHERE prenom_bdd = "Jean-Louis"; """)
    connexion.commit()
    print(curseur.fetchall())
    curseur.close()
    connexion.close()



# Affichez les données par ordre alphabétique inversé des noms de famille.
def ordre():
    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.execute(""" SELECT * FROM intervenants ORDER BY nom_bdd DESC; """)
    print(curseur.fetchall())
    curseur.close()
    connexion.close()



# Affichez les enregistrements des personnes qui ont une adresse en gmail et un nom de famille en Nouie.
def nouie():
    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.execute(""" SELECT * FROM intervenants WHERE nom_bdd ="Nouie" AND mail_bdd LIKE '%nouie%'; """)
    print(curseur.fetchall())
    curseur.close()
    connexion.close()



# Supprimez la table de la base de données.
def drop():
    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.execute(""" DROP TABLE intervenants; """)
    print(curseur.fetchall())
    connexion.commit()
    curseur.close()
    connexion.close()


# Complétez le programme en demandant à un utilisateur de saisir des données (prénom, nom, mail) et insérez ces données dans la table. L’utilisateur peut saisir plusieurs enregistrements à la suite.
def enregistrement_donnees():
    prenom = input()
    nom = input()
    mail = input()
    liste_intervenants = [
        ('Harris', 'Tote', 'h.tote@hotmail.com'),
        ('Eva', 'Nouie', 'e.nouie@gmail.com'),
        ('Tugudule', 'Niguedouille', 't.niguedouille@wanadoo.fr')]

    connexion = sqlite3.connect("base_intervenants.db")
    curseur = connexion.cursor()
    curseur.executemany("INSERT INTO intervenants VALUES(?,?,?)", liste_intervenants)     
    curseur.execute(""" INSERT INTO intervenants VALUES (prenom, nom, mail) """)
    connexion.commit()
    curseur.close()
    connexion.close()


# Faîtes la même chose pour supprimer une donnée en demandant un nom.


#gmail()
#jeanlouis()
#supprimer_jeanlouis()
#ordre()
#nouie()
#drop()
enregistrement_donnees()









