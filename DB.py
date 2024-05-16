import pymongo
connection_string = "mongodb://localhost:27017/"


class DB():
    def connectDB(self):
        conn = pymongo.MongoClient(connection_string)
        db = conn.license_plate_db
        collection = db["license_plate"]
        return collection

    def get_all_licenses(self):
        collection = self.connectDB()
        x = collection.find()
        x = list(x)
        return x

    def find_record_data(self, text):
        collection = self.connectDB()
        x = collection.find({
            '$or': [
                {'name': {'$regex': text}},
                {'license_number': {'$regex': text}}]
        })
        x= list(x)
        return x;

    def check_license(self, license):
        collection = self.connectDB()
        x_query = {"license_number": license}
        x = collection.find_one(x_query)
        return x

    def add_new_user(self, name, dob, room, license):
        collection = self.connectDB()
        collection.insert_one(
            {"name": name, "dob": dob, "room": room, "license_number": license, "time_in": "", "time_out": ""})

    def update_user(self, name, dob, room, license):
        collection = self.connectDB()
        x_query = {"license_number": license}
        new_value = {"$set": {"name": name, "dob": dob, "room": room}}
        collection.update_one(x_query, new_value)

    def delete_user(self, license):
        collection = self.connectDB()
        x_query = {"license_number": license}
        collection.delete_one(x_query)

    def update_time(self, license, time_in, time_out):
        collection = self.connectDB()
        x_query = {"license_number": license}
        new_value = {"$set": {"time_in": time_in, "time_out": time_out}}
        collection.update_one(x_query, new_value)