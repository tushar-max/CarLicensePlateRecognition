import main
import db
import easyocr

reader = easyocr.Reader(['en'], gpu=False)
collection = db.connectToDataBase()

path = './Videos/test.mp4'
print(main.detect_license_plate(path,collection,reader))