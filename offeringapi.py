from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml


app = Flask(__name__) #Instantiating it here
offering_api = Blueprint('offering_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

#-----------Offering API Calls----------------------------
@offering_api.route("/offering", methods = ['POST', 'GET', 'PUT'])
def offering():
    if request.method == 'POST':
      cur = mysql.connection.cursor()
      json = request.json

      new_ID = json['ID']

      new_Offering_ID = json['Offering_ID']
      new_Quantity_of_stock = json['Quantity_of_stock']
      new_Price_offered_at = json['Price_offered_at']
      new_Status_Complete = json['Status_Complete']
      new_Status_Incomplete = json['Status_Incomplete']

      cur.execute("INSERT INTO OFFERING(Offering_ID, ID, Quantity_of_stock, Price_offered_at, Status_Complete, Status_Incomplete) VALUES(%s, %s, %s, %s, %s, %s)", (new_Offering_ID, new_ID, new_Quantity_of_stock, new_Price_offered_at, new_Status_Complete, new_Status_Incomplete))
      
      mysql.connection.commit()
      cur.close()

      return jsonify("Offering inserted successfully")
    
    if request.method == 'GET':
        
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM OFFERING")
        
        offering_row = cur.fetchall()
        respone = jsonify({'Offering': offering_row})
        respone.status_code = 200
        
        cur.close()
        
        return respone
    
    if request.method == 'PUT':

        cur = mysql.connection.cursor()
        json = request.json
        
        new_ID = json['ID']

        new_Offering_ID = json['Offering_ID']
        new_Quantity_of_stock = json['Quantity_of_stock']
        new_Price_offered_at = json['Price_offered_at']
        new_Status_Complete = json['Status_Complete']
        new_Status_Incomplete = json['Status_Incomplete'] 

        cur.execute("UPDATE OFFERING SET Offering_ID=%s, ID = %s, Quantity_of_stock=%s, Price_offered_at=%s, Status_Complete=%s, Status_Incomplete=%s WHERE Offering_ID=%s", (new_Offering_ID, new_ID, new_Quantity_of_stock, new_Price_offered_at, new_Status_Complete, new_Status_Incomplete, new_Offering_ID))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("Offering updated successfully")

@offering_api.route("/offering/<string:Offering_ID>", methods = ['DELETE'])
def delete_offering(Offering_ID):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM OFFERING WHERE Offering_ID = %s", ([Offering_ID]))

    mysql.connection.commit()
    cur.close()
        
    return jsonify("Offering deleted successfully")

@offering_api.route("/offering/<string:Offering_ID>", methods = ['GET'])
def get_offering(Offering_ID):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM OFFERING WHERE Offering_ID = %s", ([Offering_ID]))
    specific_offering_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()
        
    return jsonify({'Offering': specific_offering_details})