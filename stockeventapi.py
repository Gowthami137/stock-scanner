from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask import Blueprint
import yaml


app = Flask(__name__) #Instantiating it here
stock_api = Blueprint('stockevent_api', __name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config ['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'
#-----------Stockevent API Calls--------------------------
#################Stockevent:##################################5555555555555555555
@app.route("/stockevent", methods=['GET', 'POST'])
def stockevent2():
    # POST
    if request.method == 'POST':
        cur = mysql.connect().cursor()
        json = request.json

        newID = json['Event_ID']
        sID = json['Stock_ID']
        newPID = json['P_ID']
        nTime = json['Time']
        nDate = json['Date']
        nBear = json['Bearish_sentiment']
        nBull = json['Bullish_sentiment']
        nNeutral = json['Neutral_sentiment']
        nChange = json['Price_Change']
        new_Predict_Stock_Events = json['Predict_Stock_Events']

        cur.execute(
            "INSERT INTO STOCKEVENT(Event_ID, Stock_ID, P_ID, Time, Date, Bearish_sentiment, Bullish_sentiment, Neutral_sentiment, Price_Change, Predict_Stock_Events) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (newID, sID, newPID, nTime, nDate, nBear, nBull, nNeutral, nChange, new_Predict_Stock_Events)
        )

        mysql.connect().commit()
        cur.close()

        return jsonify("Stockevent INSERTED successfully")
    # GET
    if request.method == 'GET':
        cur = mysql.connect().cursor()
        selectAll_stmt = "SELECT * FROM STOCKEVENT"
        cur.execute(selectAll_stmt)
        selectAll = cur.fetchall()

        cur.close()
        return jsonify({'Stockevent': selectAll})



@app.route("/stockevent/<string:event_id>", methods=['GET', 'PUT'])
def stockevent(event_id):
    # PUT
    if request.method == 'PUT':
        cur = mysql.connect().cursor()
        json = request.json

        newID = json['Event_ID']
        sID = json['Stock_ID']
        newPID = json['P_ID']
        nTime = json['Time']
        nDate = json['Date']
        nBear = json['Bearish_sentiment']
        nBull = json['Bullish_sentiment']
        nNeutral = json['Neutral_sentiment']
        nChange = json['Price_Change']
        new_Predict_Stock_Events = json['Predict_Stock_Events']

        cur.execute(
            "UPDATE STOCKEVENT SET Event_ID=%s, Stock_ID=%s, P_ID=%s, Time=%s, Date=%s, Bearish_sentiment=%s, Bullish_sentiment=%s, "
            "Neutral_sentiment=%s, Price_Change=%s Predict_Stock_Events=%s WHERE Event_ID=%s",
            (newID, sID, newPID, nTime, nDate, nBear, nBull, nNeutral, nChange, new_Predict_Stock_Events,
             event_id))

        mysql.connect().commit()
        cur.close()

        return jsonify("Stockevent UPDATED successfully")
    # GET
    if request.method == 'GET':
        cur = mysql.connect().cursor()
        select_stmt = "SELECT * FROM STOCKEVENT WHERE Event_ID = %s"
        cur.execute(select_stmt, (event_id,))
        event_Details = cur.fetchall()

        cur.close()
        return jsonify({'Stockevent': event_Details})



# ----------------------------------------End of the API Calls--------------------------------------------------------------

