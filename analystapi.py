from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml

app = Flask(__name__) #Instantiating it here
analyst_api = Blueprint('analyst_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

#-----------Analyst API Calls--------------------------
@analyst_api.route("/analyst", methods = ['POST', 'GET', 'PUT'])
def analyst():
    if request.method == 'POST':
      
      cur = mysql.connection.cursor()
      json = request.json
      
      new_ID = json['ID']
      new_Analyst_ID_Number = json['Analyst_ID_Number']
      new_Name = json['Name']
      new_Company = json['Company']      

      cur.execute("INSERT INTO ANALYST(Analyst_ID_Number, ID, Name, Company) VALUES(%s, %s, %s, %s)", (new_Analyst_ID_Number, new_ID, new_Name, new_Company))
      
      mysql.connection.commit()
      cur.close()
      
      return jsonify("Analyst inserted successfully")

    if request.method == 'GET':

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM ANALYST")
        
        analyst_row = cur.fetchall()
        respone = jsonify({'Analyst': analyst_row})
        respone.status_code = 200
        
        cur.close()
        
        return respone

    if request.method == 'PUT':

        cur = mysql.connection.cursor()
        json = request.json
        
        new_Analyst_ID_Number = json['Analyst_ID_Number']
        new_ID = json['ID']
        new_Name = json['Name']
        new_Company = json['Company']  

        cur.execute("UPDATE ANALYST SET Analyst_ID_Number=%s, ID=%s, Name=%s, Company=%s WHERE Analyst_ID_Number=%s", (new_Analyst_ID_Number, new_ID, new_Name, new_Company, new_Analyst_ID_Number))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("Analyst updated successfully")

@analyst_api.route("/analyst/<string:Analyst_ID_Number>", methods = ['DELETE'])
def delete_analyst(Analyst_ID_Number):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ANALYST WHERE Analyst_ID_Number = %s", ([Analyst_ID_Number]))

    mysql.connection.commit()
    cur.close()
        
    return jsonify("Analyst deleted successfully")

@analyst_api.route("/analyst/<string:Analyst_ID_Number>", methods = ['GET'])
def get_analyst(Analyst_ID_Number):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ANALYST WHERE Analyst_ID_Number = %s", ([Analyst_ID_Number]))
    specific_analyst_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()
        
    return jsonify({'Analyst': specific_analyst_details})