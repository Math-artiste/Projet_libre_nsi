from flask import Flask # Import de Flask dans notre programme
from flask import url_for
from flask import render_template
from flask import request

import asyncio

from akinator.async_aki import Akinator
from python.rap_citation import get_citation, ARTISTS
from random import shuffle
app = Flask(__name__) # Création de l’application web avec Flask

@app.route('/')
@app.route('/main.html/') # Route par défaut
def index(): # Fonction que Flask exécutera si il reçoit une requête ciblant la route par défaut
   return render_template('main.html')

session = {}
loop = asyncio.get_event_loop()  # Crée une instance de l'événement loop
@app.route('/akinator.html/', methods=['GET', 'POST'])
def akinator_route():
    if 'akinator_game' not in session:
        session['akinator_game'] = Akinator()

    akinator = session['akinator_game']

    if request.method == 'POST':
      button_value = request.form['button']
      if button_value == "Nouvelle partie":
        akinator.close()
        akinator_guess = loop.run_until_complete(akinator.start_game(language="fr"))

      else:
         akinator_guess = loop.run_until_complete(akinator.answer(button_value))

         if akinator.progression >= 80:
            akinator.close()
            loop.run_until_complete(akinator.win())
            try:
                  akinator_guess = f"C'est {akinator.first_guess['name']} ({akinator.first_guess['description']})!"
            except:
                  akinator_guess = "ça bug"
    else:
      akinator_guess = loop.run_until_complete(akinator.start_game(language="fr"))
    return render_template('akinator.html', button_value=akinator_guess)

artist = selectionned_artist = "laylow"
citation = ""
good_answer = ""
answers = ""
@app.route('/rap_citation.html', methods=['GET', 'POST'])
def rap_citation_route():
    global artist, selectionned_artist, citation, good_answer, answers

    if request.method == "GET":
        print("GET ICI")
        citation, answers = get_citation(selectionned_artist)
        good_answer = answers[0]
    else:
        selectionned_artist = request.form["artist"].replace(" ","")
        print(selectionned_artist, artist)
        if selectionned_artist != artist:
          artist = selectionned_artist
          citation, answers = get_citation(selectionned_artist)
          good_answer = answers[0]
        else:
            selectionned_answer = request.form["button"]
            print(selectionned_answer)
            print(selectionned_artist)
            print(good_answer)
            if selectionned_answer != good_answer.replace(" ","_"):
                print('faux')
            else:
              citation, answers = get_citation(selectionned_artist)
              good_answer = answers[0]
                
    shuffle(answers)
    return render_template('rap_citation.html', citation=citation, answers = answers, artist_list = ARTISTS,
                            selectionned_artist = selectionned_artist)
