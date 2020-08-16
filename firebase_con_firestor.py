import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore


credential_path = "/home/trex/workspace/liveplant_updates/rack_detector/Auth/ccpsl-1797d-firebase-adminsdk-333t0-02b1f5b581.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
#cred = credentials.RefreshToken('Auth/ccpsl-1797d-firebase-adminsdk-333t0-02b1f5b581.json')
default_app = firebase_admin.initialize_app()


db = firestore.client()

doc_ref = db.collection(u'counts').document(u'lpu_counts')
doc_ref.set({
    u'count_reset': 'hour:minute' ,
    u'rack_count': 'kevin_is_more_shit_shittier_than_shit',
    u'palette_count': 'Anjana_is_shit'
})
