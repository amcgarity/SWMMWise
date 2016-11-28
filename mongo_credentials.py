from pymongo import MongoClient
def mongo_credentials_aws2_AEM(database):

    mongoServer = 'mongodb://aws-2.greenphilly.net:27017/'  # aws-2 server for GreenPhilly
    client = MongoClient(mongoServer)
    
    username = "arthur"
    password = "jXlIkLfu5Dfr"
    authenticationDatabase = "admin"
    db = client[database]
    db.authenticate(username, password, source=authenticationDatabase)  # pass credentials to database
    return db
