from pymongo import MongoClient
import datetime

def connectToDataBase():
    client = MongoClient("mongodb+srv://XXXXXXX:<password>@cluster1.is5zfdn.mongodb.net/")#Connection string is hidden
    dbo = client.LisencePlates
    collection = dbo.Vehicle
    # print("Connected to MongoDb Atlas")
    return collection


def insertIntoDatabase(LicensePlateText,timestamp):
    try:
        collection = connectToDataBase()
        resultData = {
            'license_plate_text':LicensePlateText,
            'entryPoint': timestamp
        }
        collection.insert_one(resultData)
        return True
    except:
        return False

def LPExists(LicensePlateText):
    try:
        collection = connectToDataBase()
        data = collection.find_one({"license_plate_text":LicensePlateText})
        if data:
            return True
        else:
            return False
    except:
        print("Some error occured!")
        return False
    
def findAll():
    collection = connectToDataBase()
    return collection.find();
