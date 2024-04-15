from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
import yaml

from forms import RegistrationForm, LoginForm

app = Flask(__name__)  # Instantiating it here

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'

posts = [  # from the database suppose it
    {
        "ID": "MSFT",
        "StockPrice": "333.13",
        "Sector": "Technology",
        "Exchange": "NASDAQ",
    },

    {
        "ID": "AAPL",
        "StockPrice": "150.02",
        "Sector": "Technology",
        "Exchange": "NASDAQ",
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = 'testuser'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                        (username, password, permissions))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showusers'))
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'abhaykhosla0@gmail.com' and form.password == 'thisisatestforcpsc471':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your credentials again.', 'danger')
    return render_template('login.html', title='Login', form=form)


# ----------------------------------------Start of the API Calls------------------------------------------------------------
# -----------USER API Calls----------------------------

@app.route("/user/<string:username>", methods=['GET', 'PUT', 'DELETE'])
def getuser(username):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        select_stmt = "SELECT * FROM USER WHERE username = %s"
        if cur.execute(select_stmt, (username,)):
            userDetails = cur.fetchall()
            return jsonify({'username': userDetails})
        else:
            return jsonify("That User does not exist")

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_Password = json['Password']
        cur.execute("UPDATE USER SET Password=%s WHERE Username=%s",
                    (new_Password, username))

        mysql.connection.commit()
        cur.close()
        return jsonify("Password updated successfully")

    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        if cur.execute("DELETE FROM USER WHERE Username = %s", ([username])):
            mysql.connection.commit()
            cur.close()
            return jsonify("User deleted successfully")
        else:
            return jsonify("That User does not exist")


@app.route("/newuser", methods=['POST'])
def newuser():
    cur = mysql.connection.cursor()
    json = request.json

    new_Username = json['Username']
    new_Password = json['Password']
    new_Permissions = json['Permissions']

    cur.execute("INSERT INTO USER(Username, Password, Permissions) VALUES(%s, %s, %s)",
                (new_Username, new_Password, new_Permissions))
    mysql.connection.commit()
    cur.close()

    return jsonify("New User Created")


# -----------Admin API Calls----------------------------
@app.route("/admin", methods=['PUT', 'GET', 'DELETE'])
def admin():
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_Permissions = json['Permissions']
        new_User = json['Username']

        cur.execute("UPDATE USER SET Permissions=%s WHERE Username=%s",
                    (new_Permissions, new_User))

        mysql.connection.commit()
        cur.close()
        return jsonify("Permissions updated successfully")

    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        json = request.json

        new_User = json['Username']
        if cur.execute("DELETE FROM USER WHERE Username = %s", ([new_User])):
            mysql.connection.commit()
            cur.close()
            return jsonify("User deleted successfully")
        else:
            return jsonify("That User does not exist")


@app.route("/admin/usersall", methods=['GET'])
def showusers():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return jsonify({'username': userDetails})

    else:
        return jsonify("No Users In Data Base")


# -----------Private API Calls----------------------------
@app.route("/private", methods=['POST', 'PUT', 'GET', 'DELETE'])
def private():

    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        json = request.json

        new_User = json['Username']
        if cur.execute("DELETE FROM PRIVATE WHERE Username = %s", ([new_User])):
            mysql.connection.commit()
            cur.close()
            return jsonify("User deleted successfully")
        else:
            return jsonify("That User does not exist")

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        json = request.json
        new_User = json['Username']
        select_stmt = "SELECT * FROM PRIVATE WHERE Username = %s"
        cur.execute(select_stmt, (new_User,))
        listDetails = cur.fetchall()
        return jsonify({'UserDetails': listDetails})

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_username = json['Username']
        new_list = json['List_Number']
        new_role = json['Role_Type']

        cur.execute("INSERT INTO PRIVATE(List_Number, Role_Type, Username) VALUES(%s, %s, %s)",
                    (new_list, new_role, new_username))
        mysql.connection.commit()
        cur.close()

        return jsonify({new_username: "has been added to Private"})

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_username = json['Username']
        new_list = json['List_Number']

        cur.execute("UPDATE PRIVATE SET List_Number=%s WHERE Username=%s",
                    (new_list, new_username))

        mysql.connection.commit()
        cur.close()
        return jsonify("WatchList updated successfully")


# -----------Professional API Calls-------------------------
@app.route("/professional", methods=['POST', 'PUT', 'GET', 'DELETE'])
def professional():

    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        json = request.json

        new_User = json['Username']
        if cur.execute("DELETE FROM PROFESSIONAL WHERE Username = %s", ([new_User])):
            mysql.connection.commit()
            cur.close()
            return jsonify("User deleted successfully")
        else:
            return jsonify("That User does not exist")

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        json = request.json
        new_User = json['Username']
        select_stmt = "SELECT * FROM PROFESSIONAL WHERE Username = %s"
        cur.execute(select_stmt, (new_User,))
        listDetails = cur.fetchall()
        return jsonify({'UserDetails': listDetails})

    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_username = json['Username']
        new_list = json['List_Number']
        new_role = json['Role_Type']

        cur.execute("INSERT INTO PROFESSIONAL(List_Number, Role_Type, Username) VALUES(%s, %s, %s)",
                    (new_list, new_role, new_username))
        mysql.connection.commit()
        cur.close()

        return jsonify({new_username: "has been added to Professional"})

    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        new_username = json['Username']
        new_list = json['List_Number']

        cur.execute("UPDATE PROFESSIONAL SET List_Number=%s WHERE Username=%s",
                    (new_list, new_username))

        mysql.connection.commit()
        cur.close()
        return jsonify("WatchList updated successfully")

# -----------Watchlist API Calls----------------------------
@app.route("/watchlist/<string:watchlist_ID>", methods=['POST', 'GET', 'DELETE'])
def watchlist(watchlist_ID):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_Stock_ID = json['Stock_ID']

        select_stmt = "SELECT * FROM CONTAIN WHERE Watchlist_ID = %s AND Stock_ID=%s "
        cur.execute(select_stmt, (watchlist_ID, new_Stock_ID))
        msg = cur.fetchall()

        if msg:
            return jsonify({new_Stock_ID: "is already in Watchlist"})

        else:
            cur.execute("INSERT INTO CONTAIN(Stock_ID, Watchlist_ID) VALUES(%s, %s)",
                        (new_Stock_ID, watchlist_ID))
            mysql.connection.commit()
            cur.close()

            return jsonify({new_Stock_ID: "has been added to WatchList"})

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        select_stmt = "SELECT * FROM CONTAIN WHERE Watchlist_ID = %s"
        cur.execute(select_stmt, (watchlist_ID,))
        listDetails = cur.fetchall()
        return jsonify({'watchlist_ID': listDetails})

    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        json = request.json

        new_Stock_ID = json['Stock_ID']

        cur.execute("DELETE FROM CONTAIN WHERE Watchlist_ID = %s AND Stock_ID=%s", ([watchlist_ID, new_Stock_ID]))

        mysql.connection.commit()
        cur.close()

        return jsonify({new_Stock_ID: "has been deleted successfully from your Watchlist"})


@app.route("/newWatchlist", methods=['POST'])
def newList():
    cur = mysql.connection.cursor()
    json = request.json

    new_List_Number = json['List_Number']

    cur.execute("INSERT INTO WATCHLIST(List_Number) VALUES(%s)",
                (new_List_Number))
    mysql.connection.commit()
    cur.close()

    return jsonify("New Watchlist Created")


# -----------Analyst API Calls--------------------------
@app.route("/analyst", methods=['POST', 'GET', 'PUT'])
def analyst():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_ID = json['ID']
        new_Analyst_ID_Number = json['Analyst_ID_Number']
        new_Name = json['Name']
        new_Company = json['Company']

        cur.execute("INSERT INTO ANALYST(Analyst_ID_Number, ID, Name, Company) VALUES(%s, %s, %s, %s)",
                    (new_Analyst_ID_Number, new_ID, new_Name, new_Company))

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

        cur.execute("UPDATE ANALYST SET Analyst_ID_Number=%s, ID=%s, Name=%s, Company=%s WHERE Analyst_ID_Number=%s",
                    (new_Analyst_ID_Number, new_ID, new_Name, new_Company, new_Analyst_ID_Number))

        mysql.connection.commit()
        cur.close()

        return jsonify("Analyst updated successfully")


@app.route("/analyst/<string:Analyst_ID_Number>", methods=['DELETE'])
def delete_analyst(Analyst_ID_Number):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ANALYST WHERE Analyst_ID_Number = %s", ([Analyst_ID_Number]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Analyst deleted successfully")


@app.route("/analyst/<string:Analyst_ID_Number>", methods=['GET'])
def get_analyst(Analyst_ID_Number):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ANALYST WHERE Analyst_ID_Number = %s", ([Analyst_ID_Number]))
    specific_analyst_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Analyst': specific_analyst_details})


# -----------Belongs To API Calls--------------------------
@app.route("/belongsto", methods=['POST', 'GET', 'PUT'])
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


@app.route("/belongsto/<string:ID>", methods=['DELETE'])
def delete_belongsto(ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BELONGSTO WHERE ID = %s", ([ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("BelongsTo deleted successfully")


@app.route("/belongsto/<string:ID>", methods=['GET'])
def get_belongsto(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BELONGSTO WHERE ID = %s", ([ID]))
    specific_belongsto_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Belongs To': specific_belongsto_details})


# -----------Business API Calls--------------------------
@app.route("/business", methods=['POST', 'GET', 'PUT'])
def business():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_Business_ID = json['Business_ID']
        new_Address = json['Address']
        new_Founding_Date = json['Founding_Date']
        new_Business_Name = json['Business_Name']

        cur.execute("INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (new_Business_ID, new_Address, new_Founding_Date, new_Business_Name))

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

        cur.execute(
            "UPDATE BUSINESS SET Business_ID=%s, Address=%s, Founding_Date=%s, Business_Name=%s WHERE Business_ID=%s",
            (new_Business_ID, new_Address, new_Founding_Date, new_Business_Name, new_Business_ID))

        mysql.connection.commit()
        cur.close()

        return jsonify("Business updated successfully")


@app.route("/business/<string:Business_ID>", methods=['DELETE'])
def delete_business(Business_ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM BUSINESS WHERE Business_ID = %s", ([Business_ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Business deleted successfully")


@app.route("/business/<string:Business_ID>", methods=['GET'])
def get_business(Business_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([Business_ID]))
    specific_business_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Business': specific_business_details})


# -----------Exchanges API Calls--------------------------
@app.route("/exchange", methods=['POST', 'GET', 'PUT'])
def exchange():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        new_Name = json['Name']
        new_Location = json['Location']
        new_Number_of_Tickers = json['Number_of_Tickers']

        cur.execute("INSERT INTO EXCHANGES(Name, Location, Number_of_Tickers) VALUES(%s, %s, %s)",
                    (new_Name, new_Location, new_Number_of_Tickers))

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

        cur.execute("UPDATE EXCHANGES SET Name = %s, Location = %s, Number_of_Tickers = %s WHERE Name = %s",
                    (new_Name, new_Location, new_Number_of_Tickers, new_Name))

        mysql.connection.commit()
        cur.close()

        return jsonify("Exchange updated successfully")


@app.route("/exchange/<string:Name>", methods=['DELETE'])
def delete_exchange(Name):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM EXCHANGES WHERE Name = %s", ([Name]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Exchange deleted successfully")


@app.route("/exchange/<string:Name>", methods=['GET'])
def get_exchange(Name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM EXCHANGES WHERE Name = %s", ([Name]))
    specific_exchange_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Exchange': specific_exchange_details})


# -----------Offering API Calls----------------------------
@app.route("/offering", methods=['POST', 'GET', 'PUT'])
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

        cur.execute(
            "INSERT INTO OFFERING(Offering_ID, ID, Quantity_of_stock, Price_offered_at, Status_Complete, Status_Incomplete) VALUES(%s, %s, %s, %s, %s, %s)",
            (new_Offering_ID, new_ID, new_Quantity_of_stock, new_Price_offered_at, new_Status_Complete,
             new_Status_Incomplete))

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

        cur.execute(
            "UPDATE OFFERING SET Offering_ID=%s, ID = %s, Quantity_of_stock=%s, Price_offered_at=%s, Status_Complete=%s, Status_Incomplete=%s WHERE Offering_ID=%s",
            (new_Offering_ID, new_ID, new_Quantity_of_stock, new_Price_offered_at, new_Status_Complete,
             new_Status_Incomplete, new_Offering_ID))

        mysql.connection.commit()
        cur.close()

        return jsonify("Offering updated successfully")


@app.route("/offering/<string:Offering_ID>", methods=['DELETE'])
def delete_offering(Offering_ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM OFFERING WHERE Offering_ID = %s", ([Offering_ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Offering deleted successfully")


@app.route("/offering/<string:Offering_ID>", methods=['GET'])
def get_offering(Offering_ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM OFFERING WHERE Offering_ID = %s", ([Offering_ID]))
    specific_offering_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Offering': specific_offering_details})


# -----------Stock API Calls--------------------------
@app.route("/stocks", methods=['POST', 'GET', 'PUT'])
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

        cur.execute(
            "INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector))

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

        cur.execute(
            "UPDATE STOCK SET ID=%s, Company_ID=%s, Prediction_ID=%s, Predict_Stock_Price=%s, Strong_Buy=%s, Rating_Buy=%s, Rating_Sell=%s, Strong_Sell=%s, Rating_Hold=%s, Stock_Price=%s, Sector=%s WHERE ID=%s",
            (new_ID, new_Company_ID, new_Prediction_ID, new_Predict_Stock_Price, new_Strong_Buy, new_Rating_Buy,
             new_Rating_Sell, new_Strong_Sell, new_Rating_Hold, new_Stock_Price, new_Sector, new_ID))

        mysql.connection.commit()
        cur.close()

        return jsonify("Stock updated successfully")


@app.route("/stocks/<string:ID>", methods=['DELETE'])
def delete_stocks(ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM STOCK WHERE ID = %s", ([ID]))

    mysql.connection.commit()
    cur.close()

    return jsonify("Stock deleted successfully")


@app.route("/stocks/<string:ID>", methods=['GET'])
def get_stock(ID):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([ID]))
    specific_stock_details = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    return jsonify({'Stock': specific_stock_details})


#####################PR:##########################################11111111111111111
@app.route("/pr", methods=['POST', 'GET', 'PUT'])
def pr():
    # POST
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        newID = json['Event_ID']
        newPID = json['P_ID']
        new_Headline = json['Headline']
        new_Predict_PR = json['Predict_PR']

        cur.execute(
            "INSERT INTO PR(Event_ID, P_ID, Headline, Predict_PR) VALUES(%s, %s, %s, %s)",
            (newID, newPID, new_Headline, new_Predict_PR)
        )

        mysql.connection.commit()
        cur.close()

        return jsonify("PR POSTED successfully")

    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        getAll_stmt = "SELECT * FROM PR"
        cur.execute(getAll_stmt)
        getALL_Details = cur.fetchall()

        cur.close();
        return jsonify({'PR': getALL_Details})

    # PUT
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        newID = json['Event_ID']
        newPID = json['P_ID']
        new_Headline = json['Headline']
        new_Predict_PR = json['Predict_PR']

        cur.execute(
            "UPDATE PR SET Event_ID=%s, P_ID=%s, Headline=%s, Predict_PR=%s WHERE Event_ID=%s",
            (newID, newPID, new_Headline, new_Predict_PR, newID)
        )

        mysql.connection.commit()
        cur.close()

        return jsonify("PR UPDATED successfully")



@app.route("/pr/<string:event_id>", methods=['GET'])
def pr2(event_id):

    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        select_stmt = "SELECT * FROM PR WHERE Event_ID = %s"
        cur.execute(select_stmt, (event_id,))
        event_Details = cur.fetchall()

        cur.close()
        return jsonify({'PR': event_Details})

    # GET STOCK PR's


#############Prediction:##########################################2222222222222222
@app.route("/prediction", methods=['POST', 'GET', 'PUT'])
def prediction():
        # POST
        if request.method == 'POST':
            cur = mysql.connection.cursor()
            json = request.json

            newID = json['P_ID']
            cur.execute(
                "INSERT INTO PREDICTION(P_ID) VALUES (%s)",
                (newID)
            )

            mysql.connection.commit()
            cur.close()

            return jsonify("PREDICTION POSTED successfully")
        # GET
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            getAll_stmt = "SELECT * FROM PREDICTION"
            cur.execute(getAll_stmt)
            getALL_Details = cur.fetchall()

            cur.close()
            return jsonify({'Prediction': getALL_Details})

        # PUT
        if request.method == 'PUT':
            cur = mysql.connection.cursor()
            json = request.json

            newID = json['P_ID']

            cur.execute("UPDATE PREDICTION SET P_ID=%s WHERE P_ID=%s",
                        (newID, newID))

            mysql.connection.commit()
            cur.close()

            return jsonify("PREDICTION UPDATED successfully")

@app.route("/prediction/<string:p_id>", methods=['GET'])
def prediction2(p_id):

        # GET
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            select_stmt = "SELECT * FROM PREDICTION WHERE P_ID = %s"
            cur.execute(select_stmt, (p_id,))
            predict_Details = cur.fetchall()

            cur.close()
            return jsonify({'Prediction': predict_Details})



####################Secfiling##########################################333333333333
@app.route("/secfiling", methods=['GET', 'POST', 'PUT'])
def secfiling2():
    # POST
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        newID = json['Event_ID']
        newPID = json['P_ID']
        new_Type_of_Filing = json['Type_of_Filing']
        new_Predict_SEC_Filing = json['Predict_SEC_Filing']

        cur.execute(
            "INSERT INTO SECFILING(Event_ID, P_ID, Type_of_Filing, Predict_SEC_Filing) VALUES (%s, %s, %s, %s)",
            (newID, newPID, new_Type_of_Filing, new_Predict_SEC_Filing)
        )

        mysql.connection.commit()
        cur.close()

        return jsonify("SEC POSTED successfully")
    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        selectAll_stmt = "SELECT * FROM SECFILING"
        cur.execute(selectAll_stmt)
        selectAll = cur.fetchall()

        cur.close()
        return jsonify({'Secfiling': selectAll})

        # PUT
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        newID = json['Event_ID']
        newPID = json['P_ID']
        new_Type_of_Filing = json['Type_of_Filing']
        new_Predict_SEC_Filing = json['Predict_SEC_Filing']

        cur.execute(
            "UPDATE SECFILING SET Event_ID=%s, P_ID=%s, Type_of_Filing=%s, Predict_SEC_Filing=%s WHERE Event_ID=%s",
            (newID, newPID, new_Type_of_Filing, new_Predict_SEC_Filing, newID))

        mysql.connection.commit()
        cur.close()

        return jsonify("SEC UPDATED successfully")



@app.route("/secfiling/<string:event_id>", methods=['GET'])
def secfiling(event_id):

    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        select_stmt = "SELECT * FROM SECFILING WHERE Event_ID = %s"
        cur.execute(select_stmt, (event_id,))
        event_Details = cur.fetchall()

        cur.close()
        return jsonify({'SEC Filing': event_Details})

##############Week52:############################444444444444444444444444444444444
@app.route("/week52", methods=['GET', 'POST', 'PUT'])
def week52():
    # POST
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        json = request.json

        newID = json['Event_ID']
        newPID = json['P_ID']
        newValue_1 = json['Value_1']
        newTH = json['Type_High']
        newTL = json['Type_Low']
        new_Predict_52 = json['Predict_52Week']

        cur.execute(
            "INSERT INTO WEEK52(Event_ID, P_ID, Value_1, Type_High, Type_Low, Predict_52Week) VALUES (%s, %s, %s, %s, %s, %s)",
            (newID, newPID, newValue_1, newTH, newTL, new_Predict_52)
        )

        mysql.connection.commit()
        cur.close()

        return jsonify("52 Week POSTED successfully")
    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        selectAll_stmt = "SELECT * FROM WEEK52"
        cur.execute(selectAll_stmt)
        selectAll = cur.fetchall()

        cur.close()
        return jsonify({'Week52': selectAll})

        # PUT
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
        json = request.json

        newID = json['Event_ID']
        newPID = json['P_ID']
        newValue_1 = json['Value_1']
        newTH = json['Type_High']
        newTL = json['Type_Low']
        new_Predict_52 = json['Predict_52Week']

        cur.execute(
            "UPDATE WEEK52 SET Event_ID=%s, P_ID=%s, Value_1=%s, Type_High=%s, Type_Low=%s, Predict_52Week=%s WHERE Event_ID=%s",
            (newID, newPID, newValue_1, newTH, newTL, new_Predict_52, newID))

        mysql.connection.commit()
        cur.close()

        return jsonify("SEC updated successfully")



@app.route("/week52/<string:event_id>", methods=['GET'])
def week522(event_id):

    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        select_stmt = "SELECT * FROM WEEK52 WHERE Event_ID = %s"
        cur.execute(select_stmt, (event_id,))
        event_Details = cur.fetchall()

        cur.close()
        return jsonify({'Week52': event_Details})

#################Stockevent:##################################5555555555555555555
@app.route("/stockevent", methods=['GET', 'POST', 'PUT'])
def stockevent2():
    # POST
    if request.method == 'POST':
        cur = mysql.connection.cursor()
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

        mysql.connection.commit()
        cur.close()

        return jsonify("Stockevent INSERTED successfully")
    # GET
    if request.method == 'GET':
        # cur = mysql.connection.cursor()
        # selectAll_stmt = "SELECT * FROM STOCKEVENT"
        # cur.execute(selectAll_stmt)
        # selectAll = cur.fetchall()
        #
        # cur.close()
        # return jsonify({'Stockevent': selectAll})

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM STOCKEVENT")

        stocks_row = cur.fetchall()
        respone = jsonify({'Stockevent': stocks_row})
        respone.status_code = 200

        cur.close()

        return respone

    # PUT
    if request.method == 'PUT':
        cur = mysql.connection.cursor()
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
             newID))

        mysql.connection.commit()
        cur.close()

        return jsonify("Stockevent UPDATED successfully")



@app.route("/stockevent/<string:event_id>", methods=['GET'])
def stockevent(event_id):
    # GET
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        select_stmt = "SELECT * FROM STOCKEVENT WHERE Event_ID = %s"
        cur.execute(select_stmt, (event_id,))
        event_Details = cur.fetchall()

        cur.close()
        return jsonify({'Stockevent': event_Details})

# ----------------------------------------End of the API Calls--------------------------------------------------------------


if __name__ == '__main__':
    app.run(
        debug=True)  # Run it here if the name equals name, also the debug ensures that any update made here will be
    # changed here immediately onto the server