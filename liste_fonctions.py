import os
import sqlite3
import csv 
import pandas as pd
from flask import Flask, render_template

def f_insertionDonnees(donnees):
    if os.path.isfile('base_trajets.db'):
        #print("la base existe déjà.")
        
        connexion = sqlite3.connect("base_trajets.db")
        curseur = connexion.cursor()
        curseur.execute("INSERT INTO trajets VALUES(?,?,?,?,?)", donnees)
        connexion.commit()
        connexion.close()
        
    else:
        connexion = sqlite3.connect("base_trajets.db")
        curseur = connexion.cursor()
        curseur.execute("""
               CREATE TABLE trajets (
                   nom_prenom text,
                   type_vehicule text,
                   kilometrage int,
                   date numeric,
                   commentaire text
                   )
            """)
        connexion.commit()
        curseur.execute("INSERT INTO trajets VALUES(?,?,?,?,?)", donnees)
        connexion.commit()
        curseur.close()
        connexion.close()



def f_ListeChauffeurs():
    connexion = sqlite3.connect("base_trajets.db")
    curseur = connexion.cursor()
    curseur.execute(""" SELECT nom_prenom, type_vehicule, date, kilometrage FROM trajets ORDER BY date DESC """)
    liste_chauffeurs = curseur.fetchall()
    curseur.close()
    connexion.close()
    return liste_chauffeurs


def f_ChargementDonneesRH():
    connexion = sqlite3.connect("base_trajets.db")
    curseur = connexion.cursor()
    curseur.execute("""
               CREATE TABLE chauffeurs (
                   matricule integer,
                   sexe text not null,
                   nom text not null,
                   prenom text not null
                   )
            """)
    file = open('Eco_Truck_BDD_RH.csv')
    contents = csv.reader(file)
    #insert_records = "INSERT INTO chauffeurs (matricule, sexe, nom, prenom) VALUES(?, ?, ?, ?)"
    #curseur.executemany(insert_records, contents)
    #connexion.commit()
    print(contents)
    curseur.close()
    connexion.close()
    


def connexion():
    conn = sqlite3.connect('base_trajets.db')
    c = conn.cursor()
    # load the data into a Pandas DataFrame
    users = pd.read_csv('Eco_Truck_BDD_RH.csv', encoding="UTF-8")
    # write the data to a sqlite table
    users.to_sql('chauffeurs', conn, if_exists='append', index = False)
    conn.commit()
    c.execute('''SELECT * FROM chauffeurs''').fetchall()
    c.close()
    conn.close()



def liste_noms_base_rh():
    nom_fichier = "Eco_Truck_BDD_RH.csv"
    df = pd.read_csv(nom_fichier, sep = ";", encoding="ISO-8859-1")
    toto = [df.Nom[i] + " " + df.Prénom[i] for i in range(len(df))]
    return toto


def liste_vehicule_base_vehicule():
    nom_fichier = "Eco_Truck_BDD_Vehicule.csv"
    df = pd.read_csv(nom_fichier, sep = ";", encoding="ISO-8859-1")
    toto = df["Type"].unique()
    return toto


def kms_par_chauffeurs():
   connexion = sqlite3.connect("base_trajets.db")
   curseur = connexion.cursor()
   kms = curseur.execute("SELECT SUM(kilometrage) FROM trajets GROUP BY nom_prenom ORDER BY SUM(kilometrage) DESC LIMIT 3;").fetchall()
   liste_chauffeurs = curseur.execute("SELECT nom_prenom FROM trajets GROUP BY nom_prenom ORDER BY SUM(kilometrage) DESC LIMIT 3;").fetchall()

   v_tableau_kms = []
   v_tableau_chauffeurs = []
   
   #[v_tableau_kms.append(km[0]) for km in kms]
   #[v_tableau_chauffeurs.append(chauffeur[0]) for chauffeur in liste_chauffeurs]
   for km in kms:
      v_tableau_kms.append(km[0])
   for chauffeur in liste_chauffeurs:
      v_tableau_chauffeurs.append(chauffeur[0])
      
   curseur.close()
   connexion.close()
   
   return (v_tableau_chauffeurs, v_tableau_kms)


#--------------------------------------------------------------------------------------------

def kms_par_vehicule():
    
    #if os.path.isfile("base_trajets.db") :
    connexion = sqlite3.connect("base_trajets.db")
    curseur = connexion.cursor()
    kms = curseur.execute("SELECT SUM(kilometrage) FROM trajets GROUP BY type_vehicule").fetchall()
    liste_vehicules = curseur.execute("SELECT type_vehicule FROM trajets GROUP BY type_vehicule").fetchall()

    v_tableau_kms = []
    v_tableau_vehicules = []
        
    [v_tableau_kms.append(km[0]) for km in kms]
    [v_tableau_vehicules.append(vehicule[0]) for vehicule in liste_vehicules]
            
    curseur.close()
    connexion.close()
   
   # else:
    #    v_tableau_vehicules = ""
     #   v_tableau_kms = ""
       
    return (v_tableau_vehicules, v_tableau_kms)


#--------------------------------------------------------------------------------------------

def total_kms_parcourus():
   connexion = sqlite3.connect("base_trajets.db")
   curseur = connexion.cursor()
   kms = curseur.execute("SELECT SUM(kilometrage) FROM trajets ").fetchall()

   v_tableau_kms = kms[0]
   
   #[v_tableau_kms.append(km[0]) for km in kms]
      
   curseur.close()
   connexion.close()
   
   return (v_tableau_kms)


#--------------------------------------------------------------------------------------------

def kms_par_jour():
   connexion = sqlite3.connect("base_trajets.db")
   curseur = connexion.cursor()
   kms = curseur.execute("SELECT SUM(kilometrage) FROM trajets GROUP BY date").fetchall()
   dates = curseur.execute("SELECT date FROM trajets GROUP BY date").fetchall()
   
   v_tableau_kms_par_jour = []
   v_tableau_dates = []
   
   [v_tableau_kms_par_jour.append(km[0]) for km in kms]
   [v_tableau_dates.append(date[0]) for date in dates]
      
   curseur.close()
   connexion.close()
   
   return (v_tableau_kms_par_jour, v_tableau_dates)

#--------------------------------------------------------------------------------------------

def total_nombre_chauffeurs():
    if os.path.isfile('base_trajets.db'):
        connexion = sqlite3.connect("base_trajets.db")
        curseur = connexion.cursor()
        nb_chauffeurs = curseur.execute("SELECT COUNT(*) FROM trajets ").fetchall()

        v_tableau_nb_chauffeurs = nb_chauffeurs[0]
        
        # [v_tableau_kms.append(km[0]) for km in kms]
            
        curseur.close()
        connexion.close()
    else :
        v_tableau_nb_chauffeurs = ""
   
    return v_tableau_nb_chauffeurs

#--------------------------------------------------------------------------------------------

def liste_identites_base_rh():
    nom_fichier = "Eco_Truck_BDD_RH.csv"
    df = pd.read_csv(nom_fichier, sep = ";", encoding="ISO-8859-1")
    identite_chauffeurs = [(df.Nom[i] + " " + df.Prénom[i], df.Sexe[i]) for i in range(len(df))]
    return identite_chauffeurs

#--------------------------------------------------------------------------------------------