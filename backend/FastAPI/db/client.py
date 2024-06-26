from pymongo import MongoClient

# Local Database
#db_client = MongoClient().local

# Remote Database
uri = "mongodb+srv://test:test@clusterapi.zaveana.mongodb.net/?retryWrites=true&w=majority&appName=ClusterAPI"
db_client = MongoClient(uri).test
