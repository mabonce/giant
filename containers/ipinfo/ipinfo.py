import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)
db= client.db

@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/ipinfo/url_to_search' But anyway You made it here"
    return help
@app.route('/ipinfo')
@app.route('/ipinfo/<ip>')
def ipinfo(ip=''):
    findResult = findRecord(ip)
    id = findResult.get('_id')
    if (findResult is not None):
        return {"status":"Found", "id" = str(id), "result": findResult}
    lookup = "http://ipinfo.io/" + ip
    result = requests.get(lookup)
    result = json.loads(result.text)
    result['time'] = datetime.now()
    insertionResult = insertRecord(result)
    if (insertionResult['status'] != "Success"):
        return insertionResult
    insertionResult['result'] = json.loads(result.text)
    return json.dumps(insertionResult)

def insertRecord(record):
    try:
        id = db.ipinfo.insert_one(record).inserted_id
        return {"status":"Success", "id":str(id)}
    except Exception as e:
        return {"status":"Failure", "error": str(e)}

def findRecord(ip):
    try:
        record = db.ipinfo.find_one({'ip':ip})
        if (record is not None):
            return record
        else:
            return None
    except:
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002, debug=True)
