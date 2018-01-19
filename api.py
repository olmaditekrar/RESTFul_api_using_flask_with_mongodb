from flask import Flask,jsonify,request
import pymongo
# from flask.ext.mongoalchemy import MongoAlchemy
students = [{'name':'Onur Can','surname':'Yucedag'},
            {'name':'Mertcan', 'surname': 'Cetin'},
            {'name':'Mihriban','surname':'Avci'}]

app = Flask(__name__)

@app.route("/",methods=['GET'])
def hello():
    return jsonify(students)

@app.route("/students",methods=['GET'])
def getAll():
    return jsonify({'students':students})

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
        return jsonify(students)

@app.route("/students/<string:name>",methods=['PUT'])
def editOne(name):
    student = [student for student in students if student['name'] == name]
    if student == []:
        return jsonify({'Error' : 'No record for this name.'})
    else:
        student = student[0]
        student['name'] = request.get_json(force=True).get('name')
        student['surname'] = request.get_json(force=True).get('surname')
        return jsonify(students)


if __name__ == '__main__':
    app.run(debug=True,port=8080)