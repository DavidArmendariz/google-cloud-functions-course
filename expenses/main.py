import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()
db = firestore.client()


def set_expense(request):
    from datetime import datetime
    import random
    try:
        ref = db.collection('expenses').document()
        ref.set({'date': datetime.now(), 'expense': random.randint(1, 200)})
        return 'OK', 200
    except Exception as e:
        return e, 400
