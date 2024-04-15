from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml


app = Flask(__name__) #Instantiating it here
stock_api = Blueprint('stock_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'


#-----------Stock API Calls--------------------------
@stock_api.route("/stocks", methods = ['POST', 'GET', 'PUT'])
def stocks():
    if request.method == 'POST':
        
        cur = mysql.connection.cursor()
        json = request.json
        
        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']
        
        cur.execute("INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy, new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("Stock inserted successfully")
    
    if request.method == 'GET':

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM STOCK")
        
        stocks_row = cur.fetchall()
        respone = jsonify({'Stock': stocks_row})
        respone.status_code = 200
        
        cur.close()
        
        return respone 

    if request.method == 'PUT':

        cur = mysql.connection.cursor()
        json = request.json
        
        new_ID = json['ID']
        new_Company_ID = json['Company_ID']
        new_Prediction_ID = json['Prediction_ID']
        new_Predict_Stock_Price = json['Predict_Stock_Price']
        new_Strong_Buy = json['Strong_Buy']
        new_Rating_Buy = json['Rating_Buy']
        new_Rating_Sell = json['Rating_Sell']
        new_Strong_Sell = json['Strong_Sell']
        new_Rating_Hold = json['Rating_Hold']
        new_Stock_Price = json['Stock_Price']
        new_Sector = json['Sector']

        cur.execute("UPDATE STOCK SET ID=%s, Company_ID=%s, Prediction_ID=%s, Predict_Stock_Price=%s, Strong_Buy=%s, Rating_Buy=%s, Rating_Sell=%s, Strong_Sell=%s, Rating_Hold=%s, Stock_Price=%s, Sector=%s WHERE ID=%s", (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy, new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector, new_ID))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify("Stock updated successfully")

@stock_api.route("/stocks/<string:ID>", methods = ['DELETE'])
def delete_stocks(ID):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM STOCK WHERE ID = %s", ([ID]))

    mysql.connection.commit()
    cur.close()
        
    return jsonify("Stock deleted successfully")

@stock_api.route("/stocks/<string:ID>", methods = ['GET'])
def get_stock(ID):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([ID]))
    specific_stock_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()
        
    return jsonify({'Stock': specific_stock_details})