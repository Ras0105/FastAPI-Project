from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017/")
db=client["University_DB"]
students_collection=db["Students"]
print("MongoDB Connected Successfully!")