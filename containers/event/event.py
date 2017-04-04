import os
from flask import Flask, redirect, url_for, render_template, request
import json
import whois
import requests
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)
db= client.db

@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/event' But anyway You made it here"
    return help
@app.route('/event', methods=['POST'])
def event():
    event = {}
    event['name'] = request.form['name']
    event['description'] = request.form['description']
    event['AnalystComments'] = request.form['AnalystComments']
    insertionResult=insertRecord(event)
    if (insertionResult['status'] != "Success"):
        return insertionResult
    insertionResult['result'] = w
    return insertionResult


def insertRecord(record):
    try:
        id = db.event.insert_one(record).inserted_id
        return {"status":"Success", "id":id}
    except Exception as e:
        return {"status":"Failure", "error":str(e)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
