from flask import Flask # Import de Flask dans notre programme
from flask import url_for
from flask import render_template
from flask import request

import asyncio

from akinator.async_aki import Akinator
from python.rap_citation import get_citation, ARTISTS
from random import shuffle
from python.button import Quizz
app = Flask(__name__) # Création de l’application web avec Flask

@app.route('/')
@app.route('/main.html/') # Route par défaut
def index(): # Fonction que Flask exécutera si il reçoit une requête ciblant la route par défaut
   return render_template('main.html')

@app.route('/quizz_resistance', methods=['GET', 'POST'])
def quizz_ohm_route() :
  if request.method == 'GET':
    from python.resistance import random_resistance
    color = random_resistance()
    return render_template('/quizz_ressources/quizz_resistance.html', first_color = color[0][0], second_color = color[0][1], third_color = color[0][2], fourth_color = color[0][3], ohm_value= color[1][0], tolerance_value=color[1][1]) 
  else:
    ohm_answer = request.form["answer"]
    tolerance_answer = request.form["answer_t"]
    true_ohm_value = request.form["hidden_data_1"]
    true_tolerance_value = request.form["hidden_data_2"]
    if true_ohm_value == ohm_answer and true_tolerance_value == tolerance_answer :
      return render_template("/quizz_ressources/good_answer.html", final_ohm_value = true_ohm_value, final_tolerance_value= true_tolerance_value)
    else : 
      return "error"  
# @app.post("/try_answer/")
# def try_answer() :
#   ohm_answer = request.form["answer"]
#   tolerance_answer = request.form["answer_t"]
#   true_ohm_value = request.form["hidden_data_1"]
#   true_tolerance_value = request.form["hidden_data_2"]
#   if true_ohm_value == ohm_answer and true_tolerance_value == tolerance_answer :
#     return render_template("quizz_resistance.html")
#   else : 
#      return "error"
  
session = False
akinator_class = Quizz()
# akinator_class.create_buttons(buttons_content=["Non", "Probablement pas", "Je ne sais pas", "Probablement", "Oui"],
#                        buttons_value=["n","pn","idk","p","y"])
loop = asyncio.get_event_loop()  # Crée une instance de l'événement loop
@app.route('/akinator.html/', methods=['GET', 'POST'])
def akinator_route():
    global akinator
    if session != True:
        session = True
        akinator_class.akinator_game= Akinator()
    akinator_class.akinator_game
    akinator = akinator_class.akinator_game

    if request.method == 'POST':
      button_value = request.form['button']

      if button_value == "Nouvelle partie":
        loop.run_until_complete(akinator.close())
        akinator_class.question = loop.run_until_complete(akinator.start_game(language="fr"))

      else:
         akinator_class.question = loop.run_until_complete(akinator.answer(button_value))

         if akinator.progression >= 80:
            loop.run_until_complete(akinator.close())
            loop.run_until_complete(akinator.win())
            try:
                  akinator_class.question = f"C'est {akinator.first_guess['name']} ({akinator.first_guess['description']})!"
            except:
                  akinator_class.question = "ça bug"
    else:
      akinator_class.question = loop.run_until_complete(akinator.start_game(language="fr"))
    return render_template('akinator.html', akinator = akinator_class)

C_class = Quizz()
C_class.previous_artist ="Alpha Wann"
C_class.selectionned_artist ="Alpha Wann"
C_class.citation =""
C_class.good_answer =""
C_class.answers =[]
@app.route('/rap_citation.html', methods=['GET', 'POST'])
def citation_route():
    global C_class

    if request.method == "GET":
        C_class.citation, C_class.answers = get_citation(C_class.selectionned_artist)
        C_class.good_answer = C_class.answers[0]
    else:
        try:
           C_class.selectionned_artist = str(request.form["artist"]).replace(" ","-").lower()
        except:
           pass
        while C_class.selectionned_artist[-1] == "-":
           C_class.selectionned_artist = C_class.selectionned_artist[:-1]

        if C_class.selectionned_artist != C_class.previous_artist:
          C_class.previous_artist = C_class.selectionned_artist
          C_class.citation, C_class.answers = get_citation(C_class.selectionned_artist)
          C_class.good_answer = C_class.answers[0]
          shuffle(C_class.answers)

        else:
            selectionned_answer = str(request.form["button"]).lower()
            print(selectionned_answer)
            print(C_class.good_answer.lower().replace(" ",""))
            if selectionned_answer != C_class.good_answer.lower().replace(" ",""):
                print('faux')
            else:
              C_class.citation, C_class.answers = get_citation(C_class.selectionned_artist)
              C_class.good_answer = C_class.answers[0]
              shuffle(C_class.answers)
    buttons = C_class.create_buttons(buttons_content=C_class.answers, buttons_value=C_class.answers)
    print(buttons[0])
    print(buttons[0]["value"])
    return render_template('rap_citation.html', C_class=C_class, buttons = buttons, artist_list = ARTISTS)


# @app.route('/akinator.html/', methods=['GET', 'POST'])
# def flag_route():
   