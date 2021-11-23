from typing import List
#from google.cloud import firestore
from firebase_admin import firestore, credentials
import firebase_admin
import os
from schemas.tag_schema import Tag, TagId

''' Firestore configuration (to connect from Local)'''
# cred = credentials.ApplicationDefault()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
# firebase_app = firebase_admin.initialize_app(cred)
# db = firestore.Client()

'''Below line is enough to connect from Firestore from Google cloud'''
db = firestore.Client(project='fastapi-intro')


class TagDao:
    collection_name = "tags"

    def create(self, tag_create: Tag) -> Tag:
        data = tag_create.dict()
        data["id"] = str(data["id"])
        doc_ref = db.collection(
            self.collection_name).document(data["id"])
        doc_ref.set(data)
        return self.get(data["id"])

    def update(self, tag_update:Tag) -> Tag:
        data = tag_update.dict()
        print(data["id"])
        tag_doc = db.collection(
            self.collection_name).document(data["id"])
        doc= tag_doc.get()
        if doc.exists:
            tag_doc.update({ 'value': doc.to_dict()['value']+data["value"], 'updated_at': data["updated_at"] })
        else:
            tag_doc.set(data)
        print(tag_doc.get().to_dict())
        return tag_doc.get().to_dict()

    def get(self, id: TagId) -> Tag:
        doc_ref = db.collection(self.collection_name).document(str(id))
        doc = doc_ref.get()
        if doc.exists:
            return Tag(**doc.to_dict())
        return

    def list(self) -> List[Tag]:
        tag_ref = db.collection(self.collection_name)
        tag_docs = tag_ref.stream()
        tags_list = [doc.to_dict() for doc in tag_docs]
        # return [Tag(**doc.get().to_dict())
        #         for doc in tag_ref.list_documents() if doc.get().to_dict()]
        return tags_list