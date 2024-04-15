from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml

app = Flask(__name__) #Instantiating it here
exchange_api = Blueprint('exchange_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

#-----------Exchanges API Calls--------------------------
@exchange_api.route("/exchange", methods = ['POST', 'GET', 'PUT'])
def exchange():
    if request.method == 'POST':
      cur = mysql.connection.cursor()
      json = request.json
        
      new_Name = json['Name']
      new_Location = json['Location']
      new_Number_of_Tickers = json['Number_of_Tickers']
      
      cur.execute("INSERT INTO EXCHANGES(Name, Location, Number_of_Tickers) VALUES(%s, %s, %s)", (new_Name, new_Location, new_Number_of_Tickers))
      
      mysql.connection.commit()
      cur.close()
      
      return jsonify("Exchange inserted successfully")

    if request.method == 'GET':
        
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM EXCHANGES")
        
        exchange_row = cur.fetchall()
        respone = jsonify({'Exchange': exchange_row})
        respone.status_code = 200
        
        cur.close()
        
        return respone
    
    if request.method == 'PUT':

        cur = mysql.connection.cursor()
        json = request.json
        
        new_Name = json['Name']
        new_Location = json['Location']
        new_Number_of_Tickers = json['Number_of_Tickers']

        cur.execute("UPDATE EXCHANGES SET Name = %s, Location = %s, Number_of_Tickers = %s WHERE Name = %s", (new_Name, new_Location, new_Number_of_Tickers, new_Name))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("Exchange updated successfully")

@exchange_api.route("/exchange/<string:Name>", methods = ['DELETE'])
def delete_exchange(Name):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM EXCHANGES WHERE Name = %s", ([Name]))

    mysql.connection.commit()
    cur.close()
        
    return jsonify("Exchange deleted successfully")

@exchange_api.route("/exchange/<string:Name>", methods = ['GET'])
def get_exchange(Name):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EXCHANGES WHERE Name = %s", ([Name]))
    specific_exchange_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()
        
    return jsonify({'Exchange': specific_exchange_details})