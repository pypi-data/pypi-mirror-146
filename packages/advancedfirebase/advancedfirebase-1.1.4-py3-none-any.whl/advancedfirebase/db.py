#Simpe Firebase lib
#Made by Artem Lukashenko
from os import *
from firebase_admin import *


def init(database_url, credentials):
    import firebase_admin
    import json
    cred = firebase_admin.credentials.Certificate(credentials)
    def app(cred):
        import firebase_admin
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
         })
    app(cred)
def get(path):
    import firebase_admin
    from firebase_admin import db
    ref = db.reference(path)
    out = ref.get()

    return(out)
def getkey(path, key):
    import firebase_admin
    from firebase_admin import db
    ref = db.reference(path)
    out = ref.get()
    out = out[key]
    return(out)
def update(path, obj):
    import firebase_admin
    from firebase_admin import db
    ref = db.reference(path)
    ref.update(obj)
def set(path, obj):
    import firebase_admin
    from firebase_admin import db
    ref = db.reference(path)
    ref.set(obj)
def push(path, obj):
    import firebase_admin
    from firebase_admin import db
    ref = db.reference(path)
    ref.push(obj)
def parse(object, key):
    return(object[key])
def test(self):
    print('test1 passed')