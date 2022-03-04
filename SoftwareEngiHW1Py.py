from flask import Flask, render_template, request, redirect, url_for, json
import sys
import os
import socket
import requests
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://devon:bAlzytvkFQkyv5UO@cluster0.z9lh4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["people"]
collection = db["people"]

# Verify that an input is numeric and not blank
def verifyMainForm(someNum):
    if(someNum.isnumeric() != True):
        return None
    else:
        results = collection.find_one({"Id": int(someNum)})
        print(results)
        if (results == None):
            return -1
        else:
            return results

# Verify that an input is numeric
def verifyInt(someNum):
    if (someNum.isnumeric() != True):
        return None
    else:
        return int(someNum)

# Verify that an input is blank
def verifyBlank(someNum):
    if someNum == "":
        print("is blank")
        return True
    else:
        return False

# Open a json file (Currently not in use)
def getDBFile(fileName):
    opener = open(fileName)
    reader = opener.read()
    return json.loads(reader)


myApp = Flask("/")
port = 5000

# The home page
@myApp.route("/", methods = ['POST', 'GET'])
def mainpage():
    ip = "localhost:"+str(port)
    if request.method == "POST":
        user = request.form["idread"]
        user = verifyMainForm(user)
        if user == None:
            return render_template("HW1Read.html", ip = ip, message = "ERROR: Id was not a number or was blank!")
        elif user == -1:
            return render_template("HW1Read.html", name="Person Not Found", pts = -1, ip = ip)  # returns the webpage page.html and prints the audio files from audio_files
        else:
            return render_template("HW1Read.html", name=user["Name"], pts=user["Points"], ip = ip)
    else:
        return render_template("HW1Read.html", ip = ip)

# The page to create a user
@myApp.route("/create/", methods = ['POST', 'GET'])
def createpage():
    ip = "localhost:"+str(port)
    if request.method == "POST":
        id = request.form["idcreate"]
        id = verifyInt(id)
        print(id)
        name = request.form["namecreate"]
        print(name)
        score = request.form["scorecreate"]
        score = verifyInt(score)
        print(score)
        if id == None or score == None or verifyBlank(name) == True:
            return render_template("HW1Create.html", ip=ip, message = "ERROR: Id or Score was not a number or was blank!")
        else:
            if collection.find_one({"Id":id}) != None:
                return render_template("HW1Create.html", ip=ip, message="ERROR: Person with that ID already exists")
            else:
                post = {"Name": name, "Id": id, "Points": score}
                collection.insert_one(post)
                return render_template("HW1Create.html", id = id, name = name, score = score, ip=ip)
    else:
        return render_template("HW1Create.html", ip=ip)

# The page to delete a user
@myApp.route("/delete/", methods = ['POST', 'GET'])
def deletepage():
    ip = "localhost:"+str(port)
    if request.method == "POST":
        user = request.form["iddelete"]
        user = verifyMainForm(user)
        if user == None:
            return render_template("HW1Delete.html", ip = ip, message = "ERROR: Id was not a number or was blank!")
        elif user == -1:
            return render_template("HW1Delete.html", name="Person Not Found", score = -1, id = -1, ip = ip)  # returns the webpage page.html and prints the audio files from audio_files
        else:
            collection.delete_one(user)
            return render_template("HW1Delete.html", id = user["Id"], name=user["Name"], score=user["Points"], ip = ip)
    else:
        return render_template("HW1Delete.html", ip = ip)

# The page to update a user
@myApp.route("/update/", methods = ['POST', 'GET'])
def updatepage():
    ip = "localhost:"+str(port)
    if request.method == "POST":
        user = request.form["idget"]
        user = verifyMainForm(user)
        if user == None:
            return render_template("HW1Update.html", ip = ip, message = "ERROR: Get Id was not a number or was blank!")
        elif user == -1:
            return render_template("HW1Update.html", nameorig="Person Not Found", scoreorig = -1, idorig = -1, ip = ip)  # returns the webpage page.html and prints the audio files from audio_files
        else:
            nameOrig = user["Name"]
            idOrig = user["Id"]
            scoreOrig = user["Points"]
            id = request.form["idupdate"]
            name = request.form["nameupdate"]
            score = request.form["scoreupdate"]
            if verifyInt(id) == None and verifyBlank(id)==False or verifyInt(score) == None and verifyBlank(score) == False:
                return render_template("HW1Update.html", ip=ip, message="ERROR: Id or Score was not a number!")
            else:
                if(verifyBlank(id)):
                    id = idOrig
                else:
                    id = int(request.form["idupdate"])
                if (verifyBlank(score)):
                    score = scoreOrig
                else:
                    score = int(request.form["scoreupdate"])
                if (verifyBlank(name)):
                    name = nameOrig
                else:
                    name = request.form["nameupdate"]
                if collection.find_one({"Id": int(id)}) != None and int(id) != int(idOrig):
                    return render_template("HW1Update.html", ip=ip, message="ERROR: Person with that ID already exists")
                collection.update_one({"Id":idOrig}, {"$set":{"Name": name}})
                collection.update_one({"Id": idOrig}, {"$set": {"Points": score}})
                collection.update_one({"Id": idOrig}, {"$set": {"Id": id}})
                return render_template("HW1Update.html", idorig = idOrig, nameorig=nameOrig, scoreorig=scoreOrig, newid = id, newscore = score, newname = name, ip = ip)
    else:
        return render_template("HW1Update.html", ip = ip)

# The page to list every user
@myApp.route("/list/", methods = ['POST', 'GET'])
def listpage():
    ip = "localhost:"+str(port)
    return render_template("HW1List.html", collection=collection.find(), ip=ip)

if __name__ == "__main__":
    print(sys.version)
    myApp.run(debug=False, host="localhost", port=port)