from google.cloud import firestore

db = firestore.Client()

collection = db.collection('interpretervideo')
#print(db.collections())
#for c in db.collections():
   # print(c.id)
##print(collection_ref)