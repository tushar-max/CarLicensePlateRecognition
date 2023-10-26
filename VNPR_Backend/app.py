from flask import Flask,request
from flask_cors import CORS, cross_origin
import main, db
import easyocr
import json
from bson import json_util

reader = easyocr.Reader(['en'], gpu=False)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

collection = db.connectToDataBase()

@app.route('/getData',methods=['GET'])
@cross_origin()
def get_video_path():
   data = db.findAll()
   res = []
   index =0
   for i in data:
    res.append(i)
    index+=1
   return json.loads(json_util.dumps({"1":res}))

@app.route('/getPath', methods=['POST'])
@cross_origin()
def get_data():
  path = request.data
  try:
     path = request.data.decode('utf-8')
     path = path[1:-1]
   #   return path
    #  print(type(path))
     return json.loads(json_util.dumps({"1":main.detect_license_plate(path, collection,reader)})) 
#   except:
#      return ["Error"]
  except Exception as e:
     return json.loads({"error": "An error occurred during processing", "details": str(e)}), 500
  # return path
  

if __name__ == '__main__':
    app.run(debug=True)