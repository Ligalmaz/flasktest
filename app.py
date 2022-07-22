from cProfile import label
from flask import Flask, flash, render_template, url_for, request
import io
from flask import Response
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, NumberRange
import liste_fonctions as lf
import sqlite3

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = "Kaamelott"

liste_noms_prenoms =  lf.liste_noms_base_rh()
liste_type_vehicule = lf.liste_vehicule_base_vehicule()

class c_Formulaire_enregistrement_informations(FlaskForm):
  wtf_nom = SelectField('Choississez votre nom et prénom : ', choices = liste_noms_prenoms, validators = [DataRequired()])
  wtf_vehicule = SelectField(u'Choississez votre véhicule : ', choices = liste_type_vehicule, validators = [DataRequired()])
  wtf_kilometrage = IntegerField("Kilomètres réalisés : ", validators=[NumberRange(min=0, max=2000)])
  wtf_date = DateField("Date du trajet :", validators= [DataRequired()] )
  wtf_commentaire = StringField("Commentaire (facultatif) :")
  wtf_envoyer = SubmitField("Envoyer")

@app.route("/")
def f_index():
   v_texte = "Bonjour tout le monde !"
   return render_template("t_index.html", 
                          t_texte = v_texte,                      
                          t_title="Bienvenue")

@app.route("/qui_suis_je")
def f_qui_suis_je():
   v_identite = {
            "nom" : "TOU RON",
            "prenom" : "Magali"
            }
   v_titre = "Qui suis-je ? - Tout'Camion"
   v_competences = ["Gestion de projet", "Flask", "Python", "SQL", "Data analyst"]
   return render_template("t_qui_suis_je.html",
                          t_identite = v_identite,
                          t_titre = v_titre,
                          t_competences = v_competences)

#@app.route("/<v_nom>")
#def f_nom(v_nom):
#   return f"Bonjour {v_nom}"

@app.route("/mentions-legales")
def f_mentions_legales():
   v_contenu = {
      "titre" : "Mentions léagles : EkoTruck",
      "Article_loi" : "LCEN"
               }
   return render_template("t_mentions_legales.html",                                            
                          t_contenu = v_contenu)
   

@app.errorhandler(404)
def page_introuvable(e):
   return render_template("t_404.html"), 404

@app.route("/tableau_bord")
def f_tableau_bord():
   v_titre = "Tableau de bord"
   
   f_label_chauffeurs, f_kms_chauffeurs = lf.kms_par_chauffeurs()
   
   f_label_vehicules, f_kms_vehicules = lf.kms_par_vehicule()
   
   f_kms_parcourus_total = lf.total_kms_parcourus()      
   
   f_label_dates, f_kms_jours = lf.kms_par_jour()  
   
   return render_template("t_tableau_bord.html",                  
                          t_titre = v_titre,
                          t_label_chauffeurs = f_label_chauffeurs, 
                          t_kms_chauffeurs = f_kms_chauffeurs,
                          t_label_vehicules = f_label_vehicules,
                          t_kms_vehicules = f_kms_vehicules,
                          t_total_kms_parcourus = f_kms_parcourus_total,
                          t_kms_par_jour =  f_label_dates,
                          t_kms_dates = f_kms_jours)

@app.route("/rgpd")
def f_rgpd():
   v_titre = "Règlement Général sur la Protection des Données"
   return render_template("t_rgpd.html",
                          t_titre = v_titre)

@app.route("/contact", methods=['GET', 'POST'])
def f_contact():
   v_titre = "Formulaire de contact"
   f_nom = request.form.get('nom')
   f_prenom = request.form.get('prenom')
   f_email= request.form.get('adresse_email')
   f_demande= request.form.get("demande")
   return render_template("t_contact.html",
                          t_titre = v_titre, t_nom=f_nom, t_prenom=f_prenom, t_email=f_email, t_demande=f_demande)
   
#@app.route('/formulaire', methods=['GET', 'POST'])
#def f_formulaire():
#       f_nom = request.form.get('nom')
#       f_prenom = request.form.get('prenom')
#       f_age= request.form.get('age')
#       f_titre = "Formulaire"
#       return render_template('t_formulaire.html', t_age=f_age,t_nom=f_nom,t_prenom=f_prenom, t_titre=f_titre)
  
@app.route("/salaries")
def f_salaries():
   v_titre = "Liste des salariés"
   v_liste_chauffeurs = lf.f_ListeChauffeurs()
   f_nb_chauffeurs = lf.total_nombre_chauffeurs()
   v_liste_identites = lf.liste_identites_base_rh()
   return render_template("t_salaries.html",
                          t_titre = v_titre,
                          t_liste_chauffeurs = v_liste_chauffeurs,
                          t_nb_chauffeurs = f_nb_chauffeurs,
                          t_liste_identites = v_liste_identites)

@app.route("/formulaire", methods=["GET", "POST"])
def f_enregistrer_informations():
 f_formulaire = c_Formulaire_enregistrement_informations()

 if f_formulaire.validate_on_submit():
      
    f_nom = f_formulaire.wtf_nom.data
    f_formulaire.wtf_nom.data = ""
    
    f_kilometrage = f_formulaire.wtf_kilometrage.data
    f_formulaire.wtf_kilometrage.data = ""
    
    f_vehicule = f_formulaire.wtf_vehicule.data
    f_formulaire.wtf_vehicule.data = ""
    
    f_date = f_formulaire.wtf_date.data
    f_formulaire.wtf_date.data = ""
    
    f_commentaire = f_formulaire.wtf_commentaire.data
    f_formulaire.wtf_commentaire.data = ""
    
    f_donnees = (f_nom, f_vehicule, f_kilometrage, f_date, f_commentaire)
    
    lf.f_insertionDonnees(f_donnees)
       
 else :
    f_nom = ""
    f_vehicule= ""
    f_kilometrage = ""
    f_date = ""
    f_commentaire = ""

 return render_template("t_formulaire.html" ,
                          t_titre = "Formulaire d'enregistrement de vos kilomètres",
                          html_formulaire = f_formulaire,
                          t_nom=f_nom,
                          t_vehicule = f_vehicule,
                          t_kilometrage = f_kilometrage,
                          t_date = f_date,
                          t_commentaire = f_commentaire)
 

if __name__ == "__main__" :
   app.run()
