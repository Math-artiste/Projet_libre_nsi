from flask import Flask # Import de Flask dans notre programme
from flask import url_for
from flask import render_template
from flask import request

import asyncio

from akinator.async_aki import Akinator
from python.rap_citation import get_citation, ARTISTS
from random import shuffle
from python.button import Quizz
from python.flag import get_flag
app = Flask(__name__) # Création de l’application web avec Flask

@app.route('/')
@app.route('/main.html/') # Route par défaut
def index(): # Fonction que Flask exécutera si il reçoit une requête ciblant la route par défaut
   return render_template('main.html')

@app.route('/quizz_resistance.html', methods=['GET', 'POST'])
def quizz_ohm_route() :
  Score = 0
  if request.method == 'GET':
    from python.resistance import random_resistance
    color = random_resistance()
    return render_template('/quizz_ressources/quizz_resistance.html', first_color = color[0][0], second_color = color[0][1], third_color = color[0][2], fourth_color = color[0][3], ohm_value= color[1][0], tolerance_value=color[1][1], score = Score) 
  else:
    ohm_answer = request.form["answer_ohm"]
    tolerance_answer = request.form["answer_tolerance"]
    true_ohm_value = request.form["hidden_data_1"]
    true_tolerance_value = request.form["hidden_data_2"]
    if true_ohm_value == ohm_answer and true_tolerance_value == tolerance_answer :
      Score += 1
      return render_template("/quizz_ressources/good_answer.html", final_ohm_value = true_ohm_value, final_tolerance_value= true_tolerance_value)
    else : 
      return render_template("/quizz_ressources/wrong_answer.html")  
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
A_class = Quizz()
A_class.session = False
# A_class.create_buttons(buttons_content=["Non", "Probablement pas", "Je ne sais pas", "Probablement", "Oui"],
#                        buttons_value=["n","pn","idk","p","y"])
loop = asyncio.get_event_loop()  # Crée une instance de l'événement loop
@app.route('/akinator.html/', methods=['GET', 'POST'])
def akinator_route():
    global A_class
    if A_class.session != True:
        A_class.session = True
        A_class.akinator_game= Akinator()
    A_class.akinator_game
    akinator = A_class.akinator_game

    if request.method == 'POST':
      button_value = request.form['button']

      if button_value == "Nouvelle partie":
        loop.run_until_complete(akinator.close())
        A_class.question = loop.run_until_complete(akinator.start_game(language="fr"))

      else:
         A_class.question = loop.run_until_complete(akinator.answer(button_value))

         if akinator.progression >= 80:
            loop.run_until_complete(akinator.close())
            loop.run_until_complete(akinator.win())
            try:
                  A_class.question = f"C'est {akinator.first_guess['name']} ({akinator.first_guess['description']})!"
            except:
                  A_class.question = "ça bug"
    else:
      A_class.question = loop.run_until_complete(akinator.start_game(language="fr"))
    return render_template('akinator.html', akinator = A_class)

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
        C_class.attempt = 0
        C_class.success = 0
        C_class.citation, C_class.answers = get_citation(C_class.selectionned_artist)
        C_class.good_answer = C_class.answers[0].lower().replace(" ","")
        shuffle(C_class.answers)
        C_class.buttons = C_class.create_buttons(buttons_content=C_class.answers, buttons_value=C_class.answers)
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
          C_class.good_answer = C_class.answers[0].lower().replace(" ","")
          shuffle(C_class.answers)
          C_class.buttons = C_class.create_buttons(buttons_content=C_class.answers, buttons_value=C_class.answers)
        
        else:
          selectionned_answer = str(request.form["button"]).lower()
          print(selectionned_answer, C_class.good_answer)
          if selectionned_answer == "next":
            C_class.citation, C_class.answers = get_citation(C_class.selectionned_artist)
            C_class.good_answer = C_class.answers[0].lower().replace(" ","")
            shuffle(C_class.answers)
            C_class.buttons = C_class.create_buttons(buttons_content=C_class.answers, buttons_value=C_class.answers)
          elif selectionned_answer != C_class.good_answer:
              C_class.attempt += 1
              i = 0
              while selectionned_answer != C_class.answers[i].lower().replace(" ",""):
                print(C_class.answers[i].lower().replace(" ",""))
                i+=1
              C_class.buttons[i]['color'] = "btn btn-danger"
          else:
            C_class.attempt += 1
            C_class.success += 1
            i = 0
            while selectionned_answer != C_class.answers[i].lower().replace(" ",""):
                i+=1
            C_class.buttons[i]['color'] = "btn btn-success"
            C_class.buttons[-1]["available"] = True

    winrate = f"{str((round(C_class.success/C_class.attempt * 100)))}" if C_class.attempt != 0 else "0"
    return render_template('rap_citation.html', C_class=C_class, buttons = C_class.buttons, artist_list = ARTISTS, winrate=winrate)

F_class = Quizz()
@app.route('/flag.html/', methods=['GET', 'POST'])
def flag_route():
  global F_class
  if request.method == "GET":
      F_class.attempt = 0
      F_class.success = 0
      F_class.flag, F_class.answers, F_class.good_answer = get_flag()
      shuffle(F_class.answers)
      print("ANSWERS", F_class.answers)
      F_class.buttons = F_class.create_buttons(buttons_content=F_class.answers, buttons_value=F_class.answers)
      print(F_class.buttons)

  else:
      selectionned_answer = str(request.form["button"]).lower()
      if selectionned_answer == "next":
        F_class.flag, F_class.answers, F_class.good_answer = get_flag()
        F_class.good_answer = F_class.answers[0].lower().replace(" ","")
        shuffle(F_class.answers)
        F_class.buttons = F_class.create_buttons(buttons_content=F_class.answers, buttons_value=F_class.answers)
      elif selectionned_answer != F_class.good_answer:
          F_class.attempt += 1
          i = 0
          while selectionned_answer != F_class.answers[i].lower().replace(" ",""):
            print(F_class.answers[i].lower().replace(" ",""))
            i+=1
          F_class.buttons[i]['color'] = "btn btn-danger"
      else:
        F_class.attempt += 1
        F_class.success += 1
        i = 0
        while selectionned_answer != F_class.answers[i].lower().replace(" ",""):
            i+=1
        F_class.buttons[i]['color'] = "btn btn-success"
        F_class.buttons[-1]["available"] = True

  winrate = f"{str((round(F_class.success/F_class.attempt * 100)))}" if F_class.attempt != 0 else "0"
  return render_template('flag.html', F_class=F_class, buttons = F_class.buttons, winrate = winrate)
  