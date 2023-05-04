from flask import Flask # Import de Flask dans notre programme
from flask import url_for
from flask import render_template
from flask import request

app = Flask(__name__) # Création de l’application web avec Flask

@app.route('/')
@app.route('/main.html/') # Route par défaut
def index(): # Fonction que Flask exécutera si il reçoit une requête ciblant la route par défaut
   return render_template('main.html')