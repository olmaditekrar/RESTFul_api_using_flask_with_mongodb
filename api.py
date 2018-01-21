from flask import Flask,jsonify,request
import pymongo

app = Flask(__name__)
uri = 'mongodb://<accountName>:<password>@ds263137.mlab.com:63137/myexampledb'
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
    student = students.find_one({'name' : name})
    student = { 'name' : student['name'],
                'surname':student['surname']}
    return jsonify({'student' : student })

@app.route("/students",methods=['POST'])
def postStudent():
    student = {'name':request.get_json(force=True).get('name'),
               'surname':request.get_json(force=True).get('surname')}

    if students.find_one(student):
        return jsonify({'Error' : 'Already have same record.'})
    else:
        students.insert(student)
        return getAll()

@app.route("/students/<string:name>",methods=['PUT'])
def editOne(name):
    student = students.find_one({'name': name})
    if student:
        editedName = request.get_json(force=True).get('name')
        editedSurname = request.get_json(force=True).get('surname')

        if students.find_one({'name': editedName,'surname':editedSurname}):
            return jsonify({'Error':'There are already same record.'})
        else:
            students.update(student,{'name': editedName,'surname':editedSurname})
            return getAll()
    else:
        return jsonify({'Error': 'No record found for this name.'})

@app.route("/students/<string:name>",methods=['DELETE'])
def deleteOne(name):
    student = students.find_one({'name' : name})
    if student:
        students.remove(student)
        return getAll()
    else:
        return jsonify({'Error': 'No record found to delete.'})

if __name__ == '__main__':
    app.run(debug=True,port=8080)