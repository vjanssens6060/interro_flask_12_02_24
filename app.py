from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bafe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():    
    with open("data.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))      
    return render_template('index.html', data=data)
    
@app.route("/encode_info", methods=['GET', 'POST'])
def encode_info():
    if request.method == 'GET':
        return render_template('encode_info.html')

    elif request.method == 'POST':
        session['nom'] = request.form['nom']
        session['prenom'] = request.form['prenom']
        session['date_de_naissance'] = request.form['date_de_naissance']    
        session['nom_ecole'] = request.form['nom_ecole']
        session['ville_ecole'] = request.form['ville_ecole']
        session['annee'] = request.form['annee']    
        session['classe'] = request.form['classe'] 
        session['option'] = request.form['option'] 
        new_id = None

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            new_id = len(data) + 1  

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['nom'], session['prenom'], session['date_de_naissance'], session['nom_ecole'], session['ville_ecole'], session['annee'], session['classe'], session['option']]
            writer.writerow(line)
        
        return redirect('/submitted')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html',
                           nom=session['nom'],
                           prenom=session['prenom'],
                           redirect=url_for('index'),
                           delay=5000,
                           )

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        line = []
        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

            # Rechercher une ligne par son ID et modifier son contenu
            for line in data:
                if line['id'] == id:
                    nom = line['nom']
                    prenom =  line['prenom']
                    date_de_naissance = line['date_de_naissance']
                    nom_ecole = line['nom_ecole']
                    ville_ecole =  line['ville_ecole']
                    annee = line['annee']
                    classe = line['classe']
                    option =  line['option']

        return render_template('edit_info.html',
                                nom = nom,
                                prenom = prenom,
                                date_de_naissance = date_de_naissance,
                                nom_ecole = nom_ecole,
                                ville_ecole = ville_ecole,
                                annee = annee,
                                classe = classe,
                                option = option,
                                )
     
    elif request.method == 'POST':
        session['nom'] = request.form['nom']
        session['prenom'] = request.form['prenom']
        session['date_de_naissance'] = request.form['date_de_naissance']    
        session['nom_ecole'] = request.form['nom_ecole']
        session['ville_ecole'] = request.form['ville_ecole']
        session['annee'] = request.form['annee']    
        session['classe'] = request.form['classe'] 
        session['option'] = request.form['option'] 
        data = []

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

        # Rechercher une ligne par son ID et modifier son contenu
        for line in data:
            if line['id'] == id:
                line['nom'] = session['nom']
                line['prenom'] = session['prenom']
                line['date_de_naissance'] = session['date_de_naissance']
                line['nom_ecole'] = session['nom_ecole']
                line['ville_ecole'] = session['ville_ecole']
                line['annee'] = session['annee']
                line['classe'] = session['classe']
                line['option'] = session['option']

        # Réécrire le fichier CSV avec les modifications
        with open('data.csv', mode='w', newline='') as file:
            fieldnames = ['id', 'nom', 'prenom', 'date_de_naissance', 'nom_ecole', 'ville_ecole', 'annee', 'classe', 'option']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        
        return redirect('/submitted')
     

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    data = []

    with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))

    # Search for the dictionary that contains the line to be deleted
    for line in data:
        if line['id'] == id:
            # Remove the dictionary from the list
            data.remove(line)

    # Write the modified list of dictionaries to the CSV file
    with open('data.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'nom', 'prenom', 'date_de_naissance', 'nom_ecole', 'ville_ecole', 'annee', 'classe', 'option']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)
