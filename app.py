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

@app.route('/quizz_resistance', methods=['GET', 'POST'])
def quizz_ohm_route() :
  return render_template('quizz_resistance.html', first_color="red", second_color="green", third_color="black", fourth_color="grey")

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
              i = 0
              while selectionned_answer != C_class.answers[i].lower().replace(" ",""):
                print(C_class.answers[i].lower().replace(" ",""))
                i+=1
              C_class.buttons[i]['color'] = "btn btn-danger"
          else:
            i = 0
            while selectionned_answer != C_class.answers[i].lower().replace(" ",""):
                i+=1
            C_class.buttons[i]['color'] = "btn btn-success"
            C_class.buttons[-1]["available"] = True

    return render_template('rap_citation.html', C_class=C_class, buttons = C_class.buttons, artist_list = ARTISTS)

F_class = Quizz()
@app.route('/flag.html/', methods=['GET', 'POST'])
def flag_route():
  global F_class
  if request.method == "GET":
      F_class.flag, F_class.answers, F_class.good_answer = get_flag()
      shuffle(F_class.answers)
      print("ANSWERS", F_class.answers)
      F_class.buttons = F_class.create_buttons(buttons_content=F_class.answers, buttons_value=F_class.answers)
      print(F_class.buttons)

  else:
      selectionned_answer = str(request.form["button"]).lower()
      print(selectionned_answer, F_class.good_answer)
      if selectionned_answer == "next":
        F_class.flag, F_class.answers, F_class.good_answer = get_flag()
        F_class.good_answer = F_class.answers[0].lower().replace(" ","")
        shuffle(F_class.answers)
        F_class.buttons = F_class.create_buttons(buttons_content=F_class.answers, buttons_value=F_class.answers)
      elif selectionned_answer != F_class.good_answer:
          i = 0
          while selectionned_answer != F_class.answers[i].lower().replace(" ",""):
            print(F_class.answers[i].lower().replace(" ",""))
            i+=1
          F_class.buttons[i]['color'] = "btn btn-danger"
      else:
        i = 0
        while selectionned_answer != F_class.answers[i].lower().replace(" ",""):
            i+=1
        F_class.buttons[i]['color'] = "btn btn-success"
        F_class.buttons[-1]["available"] = True


  return render_template('flag.html', F_class=F_class, buttons = F_class.buttons)
  