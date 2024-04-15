from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml

app = Flask(__name__) #Instantiating it here
belongsto_api = Blueprint('belongsto_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

#-----------Belongs To API Calls--------------------------
@belongsto_api.route("/belongsto", methods = ['POST', 'GET', 'PUT'])
def belongsto():
    if request.method == 'POST':
      cur = mysql.connection.cursor()
      json = request.json
      
      new_ID = json['ID']
      new_Name = json['Name']

      cur.execute("INSERT INTO BELONGSTO(ID, Name) VALUES(%s, %s)", (new_ID, new_Name))

      mysql.connection.commit()
      cur.close()

      return jsonify("BelongsTo inserted successfully")

    if request.method == 'GET':
        
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM BELONGSTO")
        
        belongsto_row = cur.fetchall()
        respone = jsonify({'Belongs To': belongsto_row})
        respone.status_code = 200
        
        cur.close()
        
        return respone

    if request.method == 'PUT':

        cur = mysql.connection.cursor()
        json = request.json
        
        new_ID = json['ID']
        new_Name = json['Name']

        cur.execute("UPDATE BELONGSTO SET ID = %s, Name = %s Where ID = %s", (new_ID, new_Name, new_ID))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("BelongsTo updated successfully")

@belongsto_api.route("/belongsto/<string:ID>", methods = ['DELETE'])
def delete_belongsto(ID):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BELONGSTO WHERE ID = %s", ([ID]))

    mysql.connection.commit()
    cur.close()
        
    return jsonify("BelongsTo deleted successfully")

@belongsto_api.route("/belongsto/<string:ID>", methods = ['GET'])
def get_belongsto(ID):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BELONGSTO WHERE ID = %s", ([ID]))
    specific_belongsto_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()
        
    return jsonify({'Belongs To': specific_belongsto_details})