from flask import Flask, render_template, jsonify, request
import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore


app = Flask(__name__)  # Création de l'application Flask

# Route pour ajouter un point
# Connexion à la base de données
conn = sqlite3.connect("locations.db")
c = conn.cursor()

# Création de la table si elle n'existe pas
c.execute("""
    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        lat REAL,
        lon REAL
    )
""")
# Chemin vers le fichier JSON téléchargé
cred = credentials.Certificate("PIG.json")
firebase_admin.initialize_app(cred)

# Connexion à Firestore
db = firestore.client()

# Lire un document
doc = db.collection("utilisateurs").document("user1").get()
if doc.exists:
    print("Document trouvé:", doc.to_dict())
else:
    print("Pas de document trouvé.")

# Liste de points à ajouter
points = [
    ("Champs-Élysées, Paris", 48.8698, 2.3076),
    ("Montmartre, Paris", 48.8867, 2.3431),
    ("Panthéon, Paris", 48.8462, 2.3469)
]

# Insertion des points
c.executemany("INSERT INTO points (address, lat, lon) VALUES (?, ?, ?)", points)

# Enregistrer et fermer
conn.commit()
conn.close()

print("Données insérées avec succès !")
    
@app.route("/")  # Définition d'une route pour la page d'accueil
def home():
    return render_template('html_test')

@app.route("/get_points")
def get_points():
    conn = sqlite3.connect("locations.db")
    c = conn.cursor()
    c.execute("SELECT address, lat, lon FROM points")
    points = [{"address": row[0], "lat": row[1], "lon": row[2]} for row in c.fetchall()]
    
    conn.close()
    return jsonify(points)

if __name__ == "__main__":
    app.run(debug=True)  # Lancer le serveur
