import firebase_admin
from firebase_admin import firestore

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()

def set(collection,doc,data):
	doc_ref = db.collection(collection).document(doc)
	doc_ref.set(data)

def get(collection,doc):
	doc_ref = db.collection(collection).document(doc)
	data = doc_ref.get()
	if data.exists:
		return data.to_dict()
	else:
		return None

