from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml

app = Flask(__name__) #Instantiating it here
business_api = Blueprint('business_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

#-----------Business API Calls--------------------------
@business_api.route("/business", methods = ['POST', 'GET', 'PUT'])
def business():
    if request.method == 'POST':
      
      cur = mysql.connection.cursor()
      json = request.json
      
      new_Business_ID = json['Business_ID']
      new_Address = json['Address']
      new_Founding_Date = json['Founding_Date']
      new_Business_Name = json['Business_Name']
      
      cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)", (new_Business_ID, new_Address, new_Founding_Date, new_Business_Name))
      
      mysql.connection.commit()
      cur.close()
      
      return jsonify("Business inserted successfully")

    if request.method == 'GET':

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM BUSINESS")
        
        business_row = cur.fetchall()
        respone = jsonify({'Business': business_row})
        respone.status_code = 200
        
        cur.close()
        
        return respone

    if request.method == 'PUT':

        cur = mysql.connection.cursor()
        json = request.json
        
        new_Business_ID = json['Business_ID']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        cur.execute("UPDATE BUSINESS SET Business_ID=%s, Address=%s, Founding_Date=%s, Business_Name=%s WHERE Business_ID=%s", (new_Business_ID, new_Address, new_Founding_Date, new_Business_Name, new_Business_ID))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("Business updated successfully")

@business_api.route("/business/<string:Business_ID>", methods = ['DELETE'])
def delete_business(Business_ID):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BUSINESS WHERE Business_ID = %s", ([Business_ID]))

    mysql.connection.commit()
    cur.close()
        
    return jsonify("Business deleted successfully")

@business_api.route("/business/<string:Business_ID>", methods = ['GET'])
def get_business(Business_ID):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([Business_ID]))
    specific_business_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()
        
    return jsonify({'Business': specific_business_details})