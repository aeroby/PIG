import firebase_admin
from firebase_admin import credentials, firestore

# Chemin vers le fichier JSON téléchargé
cred = credentials.Certificate("chemin/vers/ta-cle.json")
firebase_admin.initialize_app(cred)

# Connexion à Firestore
db = firestore.client()

# Écrire un document
doc_ref = db.collection("utilisateurs").document("user1")
doc_ref.set({
    "nom": "Alice",
    "age": 30
})