from flask import Flask, render_template, session, redirect
import os
from questions import questions
from resultats import resultats
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    session["nb_questions"] = 0
    session["scores"] = {"Shelly":0, "Colt":0, "Bartaba":0, "Poco":0}
    return render_template("index.html")

@app.route("/questions")
def question():
    global questions
    nb_questions = session["nb_questions"]

    if nb_questions < len(questions):
        enoncé = questions[nb_questions]["enoncé"]
        questions_copy = questions[nb_questions].copy()
        questions_copy.pop("enoncé")

        reponses = list(questions_copy.values())
        clefs = list(questions_copy.keys())
        session["clefs"] = clefs
    
        return render_template("questions.html", question=enoncé, reponses=reponses)
    else:
        score_trie = sorted(session["scores"],key = session["scores"].get, reverse = True)
        nom_vainqueur = score_trie[0]
        description = resultats[nom_vainqueur]

        return render_template("resultats.html", vainqueur = nom_vainqueur, description = description)

@app.route("/reponse/<numero>")
def reponse(numero):
    session["nb_questions"] += 1
    #on recupere le nom du personnage dont la reponse a ete selectionnée
    nom_personnage = session["clefs"][int(numero)]
    session["scores"][nom_personnage] +=1
    return redirect("/questions")


app.run(host="0.0.0.0")

