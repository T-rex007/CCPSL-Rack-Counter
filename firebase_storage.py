import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os

#credential_path = "/home/trex/workspace/liveplant_updates/rack_detector/Auth/ccpsl-1797d-firebase-adminsdk-333t0-02b1f5b581.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'storageBucket': 'ccpsl-1797d.appspot.com'
})

bucket = storage.bucket()
blob = bucket.blob("LPU/lpuHistory.pdf")
blob.upload_from_filename("lpuHistory.pdf")