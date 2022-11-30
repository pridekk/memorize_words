import pymongo 

client = pymongo.MongoClient(host=['localhost:27017'], username="root", password="example")

print(client.list_database_names())

if __name__ == "__main__":
    print("test")3b241101-e2bb-4255-8caf-4136c566a962