from flask import Flask,jsonify,request
#from flask.ext.pymongo import PyMongo
# from flask.ext.mongoalchemy import MongoAlchemy
import pymongo
students = [{'name':'Onur Can','surname':'Yucedag'},
           {'name':'Mertcan', 'surname': 'Cetin'},
           {'name':'Mihriban','surname':'Avci'}]
app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'myexampledb'
# app.config['MONGO_URI'] = 'mongodb://olmaditekrar:123123124@ds263137.mlab.com:63137/myexampledb'

uri = 'mongodb://olmaditekrar:123123124@ds263137.mlab.com:63137/myexampledb'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
students = db['students']



@app.route("/students",methods=['GET'])
def getAll():
    cursor = students.find()
    allStudents = []
    for doc in cursor:
        allStudents.append({'name': doc['name'] , 'surname': doc['surname']})
    return jsonify({'students':allStudents})





@app.route("/students/<string:name>",methods=['GET'])
def getOne(name):
    student = [student for student in students if student['name']== name]
    return jsonify({'student' : student })

@app.route("/students",methods=['POST'])
def postStudent():
    student = {'name':request.get_json(force=True).get('name'),
               'surname':request.get_json(force=True).get('surname')}

    if student in students:
        return jsonify({'Error' : 'Already have same record.'})
    else:
        students.append(student)
        return jsonify({'students' : students })

@app.route("/students/<string:name>",methods=['PUT'])
def editOne(name):
    student = [student for student in students if student['name'] == name]
    if student == []:
        return jsonify({'Error' : 'No record for this name.'})
    else:
        student = student[0]
        student['name'] = request.get_json(force=True).get('name')
        student['surname'] = request.get_json(force=True).get('surname')
        return jsonify({'students' : students })


@app.route("/students/<string:name>",methods=['DELETE'])
def deleteOne(name):
    student = [student for student in students if student['name'] == name]
    if student == []:
        return jsonify({'Error' : 'No record for this name.'})
    else:
        student = student[0]
        students.remove(student)
        return jsonify({'students' : students })


if __name__ == '__main__':
    app.run(debug=True,port=8080)