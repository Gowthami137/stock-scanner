from flask import Flask, render_template, sessions, url_for, flash, redirect, request, jsonify, session
from flask.helpers import make_response
from flask_mysqldb import MySQL
from analystapi import analyst_api
from analystapi import delete_analyst
from stockapi import delete_stocks
from businessapi import delete_business
from exchangeapi import delete_exchange
from belongstoapi import belongsto_api
from businessapi import business_api
from exchangeapi import exchange_api
from offeringapi import offering_api
from stockapi import stock_api
from random import randrange

import yaml

from forms import RegistrationForm, LoginForm, DeleteFormUser, UpdateFormUser, AddFormExchange, DeleteFormExchange
from forms import UpdateFormExchange, AddFormBusiness, DeleteFormBusiness, UpdateFormBusiness, AddFormAnalyst
from forms import DeleteFormAnalyst, UpdateFormAnalyst, AddFormStock, DeleteFormStock, UpdateFormStock
from forms import DeleteFormStockWatchlist, ForgotForm, PROAddFormOffering, PROUpdateFormOffering, PRODeleteFormOffering

app = Flask(__name__)  # Instantiating it here

app.register_blueprint(analyst_api)
app.register_blueprint(belongsto_api)
app.register_blueprint(business_api)
app.register_blueprint(exchange_api)
app.register_blueprint(offering_api)
app.register_blueprint(stock_api)

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'enPOzgeOGg8bczEFhpW9XB41j3Obd9tx'


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if (existsStatus == 1):
                flash(f'Account cannot be created for {form.username.data} since it already exists!', 'danger')
                return render_template('register.html', title='Register', form=form)
            else:
                cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                            (username, password, permissions))
                flash(f'Account created for {form.username.data}!', 'success')
                if (permissions == 'Private'):
                    watchlistId = randrange(1, 10001)
                    existsStatus1 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if (existsStatus1 == 1):
                        watchlistIdNew = randrange(10001, 20000)
                        if (watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                        ([watchlistIdNew]))
                            cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                        (username, watchlistId, permissions))
                    else:
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                    ([watchlistId]))
                        cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                    (username, watchlistId, permissions))

                if (permissions == 'Professional'):
                    watchlistId = randrange(20001, 30001)
                    existsStatus2 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if (existsStatus2 == 1):
                        watchlistIdNew = randrange(30002, 40002)
                        if (watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                        ([watchlistIdNew]))
                            cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                        (username, watchlistId, permissions))
                    else:
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                    ([watchlistId]))
                        cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                    (username, watchlistId, permissions))
                mysql.connection.commit()
                cur.close()
                return redirect(url_for('login'))
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/usersall")
def showusers():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('usersall.html', title='UsersAll', userDetails=userDetails)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            usernameForm = request.form.get('username')
            passwordForm = request.form.get('password')
            userAdmin = "Admin"

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM USER Where Username = %s And Password = %s And Permissions= %s",
                        (usernameForm, passwordForm, userAdmin))
            singleUser = cur.fetchone()
            if singleUser and userAdmin == 'Admin':
                session['loggedin'] = True
                session['username'] = singleUser[0]
                flash('You have been logged in!', 'success')
                return redirect(url_for('showAdminView'))

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM USER Where Username = %s And Password = %s", (usernameForm, passwordForm))
            singleUser = cur.fetchone()
            if singleUser:
                session['loggedin'] = True
                session['username'] = singleUser[0]
                flash('You have been logged in!', 'success')
                if singleUser[2] == "Professional":
                    return redirect(url_for('showProView'))
                else:
                    return redirect(url_for('showStocks'))
            else:
                flash('Login Failed. Please check your credentials again.', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            username = request.form.get('username')
            newPassword = request.form.get('newPassword')
            confirmNewPassword = request.form.get('confirmNewPassword')

            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if (existsStatus == 0):
                flash(f'Password cannot be updated for {form.username.data} since it does not exists!', 'danger')
                return render_template('forgot.html', title='Forgot Password', form=form)
            else:
                cur.execute("UPDATE USER SET username = %s, password = %s WHERE username = %s",
                            (username, newPassword, username))
                mysql.connection.commit()
                cur.close()
                flash(f'Password updated for {form.username.data} successfully!', 'success')
                return redirect(url_for('login'))

    return render_template('forgot.html', title='Forgot Passowrd', form=form)

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/showAdminView')
def showAdminView():
    return render_template('showAdminView.html', username=session['username'])


@app.route('/addUserAdmin', methods=['GET', 'POST'])
def addUserAdmin():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if (existsStatus == 1):
                flash(f'Account cannot be created for {form.username.data} since it already exists!', 'danger')
                return render_template('register.html', title='Register', form=form)
            else:
                cur.execute("INSERT INTO USER(username, password, permissions) VALUES(%s, %s, %s)",
                            (username, password, permissions))
                flash(f'Account created for {form.username.data}!', 'success')
                if (permissions == 'Private'):
                    watchlistId = randrange(1, 10001)
                    existsStatus1 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if (existsStatus1 == 1):
                        watchlistIdNew = randrange(10001, 20000)
                        if (watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                        ([watchlistIdNew]))
                            cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                        (username, watchlistId, permissions))
                    else:
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                    ([watchlistId]))
                        cur.execute("INSERT INTO PRIVATE(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                    (username, watchlistId, permissions))

                if (permissions == 'Professional'):
                    watchlistId = randrange(20001, 30001)
                    existsStatus2 = cur.execute("SELECT * FROM Watchlist WHERE List_Number = %s", ([watchlistId]))
                    if (existsStatus2 == 1):
                        watchlistIdNew = randrange(30002, 40002)
                        if (watchlistId != watchlistIdNew):
                            cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                        ([watchlistIdNew]))
                            cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                        (username, watchlistId, permissions))
                    else:
                        cur.execute("INSERT INTO Watchlist(List_Number) VALUES(%s)",
                                    ([watchlistId]))
                        cur.execute("INSERT INTO PROFESSIONAL(username, List_Number, Role_Type) VALUES(%s, %s, %s)",
                                    (username, watchlistId, permissions))
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addUserAdmin.html', title='Add User Admin', form=form)


@app.route('/deleteUserAdmin', methods=['GET', 'POST'])
def deleteUserAdmin():
    form = DeleteFormUser()
    if form.validate_on_submit():
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if (existsStatus == 0):
                flash(f'Account cannot be deleted for {form.username.data} since it does not exist!', 'danger')
                return render_template('deleteUserAdmin.html', title='Delete User Admin', form=form)
            else:
                cur.execute("DELETE FROM USER WHERE USERNAME = %s", ([username]))
                mysql.connection.commit()
                cur.close()
                flash(f'Account deleted for {form.username.data}!', 'success')
                return redirect(url_for('showAdminView'))
    return render_template('deleteUserAdmin.html', title='Delete User Admin', form=form)


@app.route('/updateUserAdmin', methods=['GET', 'POST'])
def updateUserAdmin():
    form = UpdateFormUser()
    if form.validate_on_submit():
        if request.method == 'POST':
            userDetails = request.form
            username = userDetails['username']
            password = userDetails['password']
            permissions = request.form['user_type']
            cur = mysql.connection.cursor()
            existStatus = cur.execute("SELECT * FROM USER WHERE USERNAME = %s", ([username]))
            if (existStatus == 0):
                flash(f'Account cannot be updated for {form.username.data} since it does not exist!', 'danger')
                return render_template('updateUserAdmin.html', title='Update User Admin', form=form)
            else:
                cur.execute("UPDATE USER SET username = %s, password = %s, permissions = %s WHERE username = %s",
                            (username, password, permissions, username))
                mysql.connection.commit()
                cur.close()
                flash(f'Account updated for {form.username.data} successfully!', 'success')
                return redirect(url_for('showAdminView'))
    return render_template('updateUserAdmin.html', title='Update User Admin', form=form)


@app.route('/addExchangeAdmin', methods=['GET', 'POST'])
def addExchangeAdmin():
    form = AddFormExchange()
    if form.validate_on_submit():
        if request.method == 'POST':
            exchangeDetails = request.form
            name = exchangeDetails['name']
            location = exchangeDetails['location']
            numberOfTickers = request.form['number_of_tickers']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM EXCHANGES WHERE NAME = %s", ([name]))
            if (existsStatus == 1):
                flash(f'Exchange with the name {form.name.data} cannot be created since it already exists!', 'danger')
                return render_template('addExchangeAdmin.html', title='Add Exchange Admin', form=form)
            else:
                cur.execute("INSERT INTO EXCHANGES(Name, Location, Number_of_Tickers) VALUES(%s, %s, %s)",
                            (name, location, numberOfTickers))
                flash(f'Exchange with the name {form.name.data} created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addExchangeAdmin.html', title='Add Exchange Admin', form=form)


@app.route('/deleteExchangeAdmin', methods=['GET', 'POST'])
def deleteExchangeAdmin():
    form = DeleteFormExchange()
    if form.validate_on_submit():
        if request.method == 'POST':
            exchangeDetails = request.form
            name = exchangeDetails['name']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM EXCHANGES WHERE NAME = %s", ([name]))
            if (existsStatus == 0):
                flash(f'Exchange with the name {form.name.data} does not exist!', 'danger')
                return render_template('deleteExchangeAdmin.html', title='Delete Exchange Admin', form=form)
            else:
                delete_exchange(name)
                flash(f'Exchange with the name {form.name.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('deleteExchangeAdmin.html', title='Delete Exchange Admin', form=form)


@app.route('/updateExchangeAdmin', methods=['GET', 'POST'])
def updateExchangeAdmin():
    form = UpdateFormExchange()
    if form.validate_on_submit():
        if request.method == 'POST':
            exchangeDetails = request.form
            cur = mysql.connection.cursor()
            name = exchangeDetails['name']
            location = exchangeDetails['location']
            numberOfTickers = request.form['number_of_tickers']
            existsStatus = cur.execute("SELECT * FROM EXCHANGES WHERE NAME = %s", ([name]))
            if (existsStatus == 0):
                flash(f'Exchange with the name {form.name.data} cannot be updated since it does not exists!', 'danger')
                return render_template('updateExchangeAdmin.html', title='Update Exchange Admin', form=form)
            else:
                cur.execute("UPDATE EXCHANGES SET Name = %s, Location = %s, Number_of_Tickers = %s WHERE Name = %s",
                            (name, location, numberOfTickers, name))
                flash(f'Exchange with the name {form.name.data} updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('updateExchangeAdmin.html', title='Update Exchange Admin', form=form)


@app.route('/showExchangeAdmin')
def showExchangeAdmin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM EXCHANGES")
    if resultValue > 0:
        exchangeDetails = cur.fetchall()

    return render_template('showExchanges.html', title='Show Exchanges Admin', exchangeDetails=exchangeDetails)


@app.route('/addBusinessAdmin', methods=['GET', 'POST'])
def addBusinessAdmin():
    form = AddFormBusiness()
    if form.validate_on_submit():
        if request.method == 'POST':
            businessDetails = request.form
            business_id = businessDetails['business_id']
            address = businessDetails['address']
            founding_date = businessDetails['founding_date']
            business_name = businessDetails['business_name']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([business_id]))
            if (existsStatus == 1):
                flash(f'Business with the name {form.business_name.data} cannot be created since it already exists!',
                      'danger')
                return render_template('addBusinessAdmin.html', title='Add Business Admin', form=form)
            else:
                cur.execute(
                    "INSERT INTO BUSINESS(Business_ID, Address, Founding_Date, Business_Name) VALUES(%s, %s, %s, %s)",
                    (business_id, address, founding_date, business_name))
                flash(f'Business with the name {form.business_name.data} created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addBusinessAdmin.html', title='Add Business Admin', form=form)


@app.route('/deleteBusinessAdmin', methods=['GET', 'POST'])
def deleteBusinessAdmin():
    form = DeleteFormBusiness()
    if form.validate_on_submit():
        if request.method == 'POST':
            businessDetails = request.form
            business_id = businessDetails['business_id']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([business_id]))
            if (existsStatus == 0):
                flash(f'Business with the ID {form.business_id.data} does not exist!', 'danger')
                return render_template('deleteBusinessAdmin.html', title='Delete Business Admin', form=form)
            else:
                delete_business(business_id)
                flash(f'Business with the ID {form.business_id.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('deleteBusinessAdmin.html', title='Delete Business Admin', form=form)


@app.route('/updateBusinessAdmin', methods=['GET', 'POST'])
def updateBusinessAdmin():
    form = UpdateFormBusiness()
    if form.validate_on_submit():
        if request.method == 'POST':
            businessDetails = request.form
            business_id = businessDetails['business_id']
            address = businessDetails['address']
            founding_date = businessDetails['founding_date']
            business_name = businessDetails['business_name']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM BUSINESS WHERE Business_ID = %s", ([business_id]))
            if (existsStatus == 0):
                flash(f'Business with the name {form.business_name.data} cannot be updated since it does not exists!',
                      'danger')
                return render_template('updateBusinessAdmin.html', title='Update Business Admin', form=form)
            else:
                cur.execute(
                    "UPDATE BUSINESS SET Business_ID=%s, Address=%s, Founding_Date=%s, Business_Name=%s WHERE Business_ID=%s",
                    (business_id, address, founding_date, business_name, business_id))
                flash(f'Business with the name {form.business_name.data} updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('updateBusinessAdmin.html', title='Update Business Admin', form=form)


@app.route('/showBusinessAdmin')
def showBusinessAdmin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM BUSINESS")
    if resultValue > 0:
        businessDetails = cur.fetchall()

    return render_template('showBusinesses.html', title='Show Businesses Admin', businessDetails=businessDetails)


@app.route('/addAnalystAdmin', methods=['GET', 'POST'])
def addAnalystAdmin():
    form = AddFormAnalyst()
    if form.validate_on_submit():
        if request.method == 'POST':
            analystDetails = request.form
            analyst_id_number = analystDetails['analyst_id_number']
            stock_id = analystDetails['stock_id']
            analyst_name = analystDetails['analyst_name']
            analyst_company = analystDetails['analyst_company']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM ANALYST WHERE Analyst_ID_Number = %s", ([analyst_id_number]))
            if (existsStatus == 1):
                flash(f'Analyst with the name {form.analyst_name.data} cannot be created since it already exists!',
                      'danger')
                return render_template('addAnalystAdmin.html', title='Add Analyst Admin', form=form)
            else:
                cur.execute("INSERT INTO ANALYST(Analyst_ID_Number, ID, Name, Company) VALUES(%s, %s, %s, %s)",
                            (analyst_id_number, stock_id, analyst_name, analyst_company))
                flash(f'Analyst with the name {form.analyst_name.data} created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addAnalystAdmin.html', title='Add Analyst Admin', form=form)


@app.route('/deleteAnalystAdmin', methods=['GET', 'POST'])
def deleteAnalystAdmin():
    form = DeleteFormAnalyst()
    if form.validate_on_submit():
        if request.method == 'POST':
            analystDetails = request.form
            analyst_id_number = analystDetails['analyst_id_number']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM ANALYST WHERE Analyst_ID_Number = %s", ([analyst_id_number]))
            if (existsStatus == 0):
                flash(f'Analyst with the ID {form.analyst_id_number.data} does not exist!', 'danger')
                return render_template('deleteAnalystAdmin.html', title='Delete Analyst Admin', form=form)
            else:
                delete_analyst(analyst_id_number)
                flash(f'Analyst with the ID {form.analyst_id_number.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('deleteAnalystAdmin.html', title='Delete Analyst Admin', form=form)


@app.route('/updateAnalystAdmin', methods=['GET', 'POST'])
def updateAnalystAdmin():
    form = UpdateFormAnalyst()
    if form.validate_on_submit():
        if request.method == 'POST':
            analystDetails = request.form
            analyst_id_number = analystDetails['analyst_id_number']
            stock_id = analystDetails['stock_id']
            analyst_name = analystDetails['analyst_name']
            analyst_company = analystDetails['analyst_company']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM ANALYST WHERE Analyst_ID_Number = %s", ([analyst_id_number]))
            if (existsStatus == 0):
                flash(f'Analyst with the name {form.analyst_name.data} cannot be updated since it does not exists!',
                      'danger')
                return render_template('updateAnalystAdmin.html', title='Update Analyst Admin', form=form)
            else:
                cur.execute(
                    "UPDATE ANALYST SET Analyst_ID_Number=%s, ID=%s, Name=%s, Company=%s WHERE Analyst_ID_Number=%s",
                    (analyst_id_number, stock_id, analyst_name, analyst_company, analyst_id_number))
                flash(f'Analyst with the name {form.analyst_name.data} updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('updateAnalystAdmin.html', title='Update Analyst Admin', form=form)


@app.route('/showAnalystAdmin')
def showAnalystAdmin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM ANALYST")
    if resultValue > 0:
        analystDetails = cur.fetchall()

    return render_template('showAnalysts.html', title='Show Analyst Admin', analystDetails=analystDetails)


@app.route('/addStockAdmin', methods=['GET', 'POST'])
def addStockAdmin():
    form = AddFormStock()
    if form.validate_on_submit():
        if request.method == 'POST':
            stockDetails = request.form
            stock_id = stockDetails['stock_id']
            company_id = stockDetails['company_id']
            prediction_id = stockDetails['prediction_id']
            predict_stock_price = stockDetails['predict_stock_price']
            strong_buy = stockDetails['strong_buy']
            rating_buy = stockDetails['rating_buy']
            rating_sell = stockDetails['rating_sell']
            strong_sell = stockDetails['strong_sell']
            rating_hold = stockDetails['rating_hold']
            stock_price = stockDetails['stock_price']
            sector = stockDetails['sector']
            belongs_to = stockDetails['belongs_to']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([stock_id]))
            if (existsStatus == 1):
                flash(f'Stock with the ID {form.stock_id.data} cannot be created since it already exists!', 'danger')
                return render_template('addStockAdmin.html', title='Add Stock Admin', form=form)
            else:
                cur.execute(
                    "INSERT INTO STOCK(ID, Company_ID, Prediction_ID, Predict_Stock_Price, Strong_Buy, Rating_Buy, Rating_Sell, Strong_Sell, Rating_Hold, Stock_Price, Sector) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (stock_id, company_id, prediction_id, predict_stock_price, strong_buy, rating_buy, rating_sell,
                     strong_sell, rating_hold, stock_price, sector))
                cur.execute(
                    "INSERT INTO BELONGSTO(ID, Name) VALUES(%s, %s)",
                    (stock_id, belongs_to))                    
                flash(f'Stock with the ID {form.stock_id.data} created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('addStockAdmin.html', title='Add Stock Admin', form=form)


@app.route('/deleteStockAdmin', methods=['GET', 'POST'])
def deleteStockAdmin():
    form = DeleteFormStock()
    if form.validate_on_submit():
        if request.method == 'POST':
            stockDetails = request.form
            stock_id = stockDetails['stock_id']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([stock_id]))
            if (existsStatus == 0):
                flash(f'Stock with the ID {form.stock_id.data} does not exist!', 'danger')
                return render_template('deleteStockAdmin.html', title='Delete Stock Admin', form=form)
            else:
                delete_stocks(stock_id)
                flash(f'Stock with the ID {form.stock_id.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('deleteStockAdmin.html', title='Delete Stock Admin', form=form)


@app.route('/updateStockAdmin', methods=['GET', 'POST'])
def updateStockAdmin():
    form = UpdateFormStock()
    if form.validate_on_submit():
        if request.method == 'POST':
            stockDetails = request.form
            stock_id = stockDetails['stock_id']
            company_id = stockDetails['company_id']
            prediction_id = stockDetails['prediction_id']
            predict_stock_price = stockDetails['predict_stock_price']
            strong_buy = stockDetails['strong_buy']
            rating_buy = stockDetails['rating_buy']
            rating_sell = stockDetails['rating_sell']
            strong_sell = stockDetails['strong_sell']
            rating_hold = stockDetails['rating_hold']
            stock_price = stockDetails['stock_price']
            sector = stockDetails['sector']
            belongs_to = stockDetails['belongs_to']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([stock_id]))
            if (existsStatus == 0):
                flash(f'Stock with the ID {form.stock_id.data} cannot be updated since it does not exists!', 'danger')
                return render_template('updateStockAdmin.html', title='Update Stock Admin', form=form)
            else:
                cur.execute(
                    "UPDATE STOCK SET ID=%s, Company_ID=%s, Prediction_ID=%s, Predict_Stock_Price=%s, Strong_Buy=%s, Rating_Buy=%s, Rating_Sell=%s, Strong_Sell=%s, Rating_Hold=%s, Stock_Price=%s, Sector=%s WHERE ID=%s",
                    (stock_id, company_id, prediction_id, predict_stock_price, strong_buy, rating_buy, rating_sell,
                     strong_sell, rating_hold, stock_price, sector, stock_id))
                cur.execute(
                    "UPDATE BELONGSTO SET ID = %s, Name=%s WHERE ID = %s and Name=%s",
                    (stock_id, belongs_to,stock_id, belongs_to))         
                flash(f'Stock with the ID {form.stock_id.data} updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showAdminView'))
    return render_template('updateStockAdmin.html', title='Update Stock Admin', form=form)


@app.route('/showStockAdmin')
def showStockAdmin():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM STOCK")
    if resultValue > 0:
        stockDetails = cur.fetchall()

    return render_template('showStocksAdmin.html', title='Show Stock Admin', stockDetails=stockDetails)


@app.route('/showStocks')
def showStocks():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM STOCK")
    if resultValue > 0:
        stockDetails = cur.fetchall()

    return render_template('showStocks.html', username=session['username'], stockDetails=stockDetails)


@app.route("/stockInformation/<string:ID>", methods=['GET', 'POST'])
def showStockInformation(ID):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM STOCK WHERE ID = %s", ([ID]))
        stockDetails = cur.fetchone()

        resultValue = cur.execute("SELECT * FROM STOCKEVENT WHERE STOCK_ID = %s", ([ID]))
        if resultValue > 0:
            dateDetails = cur.fetchall()
        else:
            dateDetails = resultValue

        resultValue = cur.execute("SELECT * FROM STOCKEVENT WHERE STOCK_ID = %s", ([ID]))
        if resultValue > 0:
            sDetails = cur.fetchone()
            newPID = sDetails[2]
            cur.execute("SELECT * FROM PR WHERE P_ID = %s", ([newPID]))
            prDetails = cur.fetchall()

        else:
            prDetails = resultValue

        result= cur.execute("SELECT * FROM ANALYST WHERE ID = %s", ([ID]))
        if result > 0:
            analystDetails = cur.fetchall()
        else:
            analystDetails = result

        return render_template('stockInformation.html', username=session['username'], stockDetails=stockDetails,
                               dateDetails=dateDetails, prDetails=prDetails, analystDetails=analystDetails)


@app.route('/watchlistDetails', methods=['GET', 'POST'])
def showWatchlist():
    cur = mysql.connection.cursor()
    new_User = session['username']

    select_stmt = "SELECT List_Number FROM PRIVATE WHERE Username = %s"
    resultValue = cur.execute(select_stmt, (new_User,))
    if resultValue > 0:
        listDetails = cur.fetchall()
        newWatchlist = listDetails

    # if listDetail < 0 then scan PRIVATE
    if resultValue <= 0:
        select_stmt = "SELECT List_Number FROM PROFESSIONAL WHERE Username = %s"
        resultValue = cur.execute(select_stmt, (new_User,))
        if resultValue > 0:
            listDetails = cur.fetchall()
            newWatchlist = listDetails
    # newWatchlist > 0 scan for watchlist
    if resultValue > 0:
        if request.method == 'POST':
            post_id = request.form.get('postStock')
            select_stmt = "SELECT * FROM CONTAIN WHERE Watchlist_ID = %s AND Stock_ID=%s "
            cur.execute(select_stmt, (newWatchlist, post_id))
            msg = cur.fetchall()
            if not msg:
                cur.execute("INSERT INTO CONTAIN(Stock_ID, Watchlist_ID) VALUES(%s, %s)",
                            (post_id, newWatchlist))
                mysql.connection.commit()

        if request.method == 'DELETE':
            text = request.form['text']
            processed_text = text.upper()
            cur.execute("DELETE FROM CONTAIN WHERE Watchlist_ID = %s AND Stock_ID=%s", ([newWatchlist, processed_text]))
            mysql.connection.commit()
            cur.close()

        cur.execute("SELECT * FROM CONTAIN WHERE Watchlist_ID = %s", ([newWatchlist]))
        allListDetails = cur.fetchall()

    else:
        allListDetails = resultValue

    # add listDetails to render then make an if statment to check if it exists  if not "contact admin to make watchlist"
    return render_template('watchlist.html', username=session['username'], allListDetails=allListDetails,
                           resultValue=resultValue, listDetails=listDetails)


@app.route('/deleteStockWatchlist/<string:ID>', methods=['GET', 'POST'])
def deleteStockWatchlist(ID):
    watchlist = ID
    cur = mysql.connection.cursor()
    form = DeleteFormStockWatchlist()
    if form.validate_on_submit():
        if request.method == 'POST':
            stockDetails = request.form
            stock_id = stockDetails['stock_id']

            existsStatus = cur.execute("DELETE FROM CONTAIN WHERE Watchlist_ID = %s AND Stock_ID=%s",
                                       ([watchlist, stock_id]))
            if (existsStatus == 0):
                flash(f'Stock with the ID {form.stock_id.data} does not exist!', 'danger')
                return render_template('deleteStockWatchlist.html', title='Delete Stock Watchlist', form=form)
            else:
                flash(f'Stock with the ID {form.stock_id.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showWatchlist'))
    return render_template('deleteStockWatchlist.html', title='Delete Stock Watchlist', form=form)


@app.route('/eventDetails')
def showEvents():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM STOCKEVENT")
    if resultValue > 0:
        eventDetails1 = cur.fetchall()
    return render_template('event.html', username=session['username'], eventDetails1=eventDetails1)


@app.route('/prDetails')
def showPR():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT HEADLINE FROM PR")
    if resultValue > 0:
        prDetails1 = cur.fetchall()
    else:
        return render_template('prMissing.html', title='News Section', username=session['username'])
    return render_template('pr.html', title='News Section', username=session['username'], prDetails1=prDetails1)


@app.route('/week52Details')
def showWeek52():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM BUSINESS")
    if resultValue > 0:
        businessIDDetails = cur.fetchall()
    resultValue1 = cur.execute("SELECT * FROM Week52")
    if resultValue1 > 0:
        week52Details1 = cur.fetchall()
    return render_template('week52.html', title='Week 52 Section', username=session['username'],
                           businessIDDetails=businessIDDetails, week52Details1=week52Details1)

@app.route('/showSecFiling')
def showSecFiling():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM SECFILING")
    if resultValue > 0:
        secFilingDetails = cur.fetchall()
    return render_template('secFiling.html', title='Section Filing', username=session['username'],
                           secFilingDetails=secFilingDetails)

@app.route('/showOffering')
def showOffering():
    return render_template('offering.html', title='Offering', username=session['username'])
@app.route('/showProView')
def showProView():
    return render_template('showProView.html', title='Professional View', username=session['username'])

@app.route('/PROaddOffering', methods=['GET', 'POST'])
def PROaddOffering():
    form = PROAddFormOffering()
    if form.validate_on_submit():
        if request.method == 'POST':
            offeringDetails = request.form
            offeringID = offeringDetails['offeringID']
            iD = offeringDetails['iD']
            offer_quant = offeringDetails['offer_quant']
            offer_price = offeringDetails['offer_price']
            statusComplete = offeringDetails['statusComplete']
            statusNotComplete = offeringDetails['statusNotComplete']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM OFFERING WHERE Offering_ID = %s", ([offeringID]))
            if (existsStatus == 1):
                flash(f'Offering with the ID cannot be created since it already exists!',
                      'danger')
                return render_template('PROaddOffering.html', title='Add Offering', form=form)
            else:
                cur.execute(
                    "INSERT INTO OFFERING(Offering_ID, ID, Quantity_of_stock, Price_offered_at, Status_Complete, Status_Incomplete) VALUES(%s, %s, %s, %s, %s, %s)",
                    (offeringID, iD, offer_quant, offer_price, statusComplete, statusNotComplete))
                flash(f'OFFERING created successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showOffering'))
    return render_template('PROaddOffering.html', title='Add Offering', form=form)

@app.route('/PROupdateOffering', methods=['GET', 'POST'])
def PROupdateOffering():
     form = PROUpdateFormOffering()
     if form.validate_on_submit():
        if request.method == 'POST':
            offeringDetails = request.form
            offeringID = offeringDetails['offeringID']
            statusComplete = offeringDetails['statusComplete']
            statusNotComplete = offeringDetails['statusNotComplete']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM OFFERING WHERE Offering_ID = %s", ([offeringID]))
            if (existsStatus == 0):
                flash(f'Offering with the ID cannot be updated since it does not exists!',
                      'danger')
                return render_template('PROupdateOffering.html', title='Update Offering', form=form)
            else:
                cur.execute(
                    "UPDATE OFFERING SET Status_Complete=%s, Status_Incomplete=%s WHERE Offering_ID=%s",
                    (statusComplete, statusNotComplete, offeringID))
                flash(f'OFFERING Updated successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showOffering'))
     return render_template('PROupdateOffering.html', title='Update Offering', form=form)

@app.route('/PROshowOffering')
def PROshowOffering():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM OFFERING")
    if resultValue > 0:
        offering = cur.fetchall()

    return render_template('PROshowOffering.html', title='Show Offering', offering=offering)

@app.route('/PROdeleteOffering', methods=['GET', 'POST'])
def PROdeleteOffering():
    form = PRODeleteFormOffering()
    if form.validate_on_submit():
        if request.method == 'POST':
            offeringDetails = request.form
            offerID = offeringDetails['offerID']
            cur = mysql.connection.cursor()
            existsStatus = cur.execute("SELECT * FROM OFFERING WHERE Offering_ID = %s", ([offerID]))
            if (existsStatus == 0):
                flash(f'Offering with the ID {form.offerID.data} does not exist!', 'danger')
                return render_template('PROdeleteOffering.html', title='Delete Offering', form=form)
            else:
                cur = mysql.connection.cursor()
                cur.execute("DELETE FROM OFFERING WHERE Offering_ID = %s", ([offerID]))

                mysql.connection.commit()
                cur.close()
                flash(f'Offering with the ID {form.offerID.data} deleted successfully!', 'success')
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('showOffering'))
    return render_template('PROdeleteOffering.html', title='Delete Offering', form=form)
if __name__ == '__main__':
    app.run(
        debug=True)  # Run it here if the name equals name, also the debug ensures that any update made here will be
    # changed here immediately onto the server