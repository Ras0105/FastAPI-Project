from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017/")
# MongoDB Atlas
# client=MongoClient("mongodb+srv://Ras0105:<db_password>@cluster0.nf7ib5e.mongodb.net/?appName=Cluster0")
db=client["University_DB"]
students_collection=db["Students"]
print("MongoDB Connected Successfully!")