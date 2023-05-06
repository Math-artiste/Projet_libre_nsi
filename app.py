from flask import Flask # Import de Flask dans notre programme
from flask import url_for
from flask import render_template
from flask import request

from python.akinator import Akinator as Akinator_class, akinator_guess
import asyncio

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
        session['akinator_game'] = Akinator_class()

    akinator = session['akinator_game']

    if request.method == 'POST':
      button_value = request.form['button']
      if button_value == "Nouvelle partie":
        akinator.close()
        akinator_guess = loop.run_until_complete(session['akinator_game'].start_game(language="fr"))

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
      akinator_guess = loop.run_until_complete(session['akinator_game'].start_game(language="fr"))
    return render_template('akinator.html', button_value=akinator_guess)