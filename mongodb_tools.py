from bson.objectid import ObjectId
import binascii

def mongo_doc_id_from_string(DocIdString):
    binaryDocId = binascii.unhexlify(DocIdString)
    mongoDocId = ObjectId(binaryDocId)   
    return mongoDocId
