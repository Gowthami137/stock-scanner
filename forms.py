from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=20)])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=20)])

    submit = SubmitField('Login')


class DeleteFormUser(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Delete User')


class UpdateFormUser(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=20)])

    submit = SubmitField('Update User')

class ForgotForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=25)])

    newPassword = PasswordField('New Password',
                             validators=[DataRequired(), Length(min=8, max=20)])
    
    confirmNewPassword = PasswordField('Confirm New Password',
                             validators=[DataRequired(), Length(min=8, max=20)])

    submit = SubmitField('Update Password')

class AddFormExchange(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=25)])

    location = StringField('Location',
                           validators=[DataRequired(), Length(min=2, max=25)])

    number_of_tickers = IntegerField('Number of Tickers',
                                     validators=[DataRequired()])

    submit = SubmitField('Add Exchange')


class DeleteFormExchange(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Delete Exchange')


class UpdateFormExchange(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=25)])

    location = StringField('Location',
                           validators=[DataRequired(), Length(min=2, max=25)])

    number_of_tickers = IntegerField('Number of Tickers',
                                     validators=[DataRequired()])

    submit = SubmitField('Update Exchange')


class AddFormBusiness(FlaskForm):
    business_id = StringField('Business ID',
                              validators=[DataRequired(), Length(min=2, max=4)])

    address = StringField('Address',
                          validators=[DataRequired(), Length(min=2, max=45)])

    founding_date = StringField('Founding Date',
                                validators=[DataRequired(), Length(min=2, max=25)])

    business_name = StringField('Business Name',
                                validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Add Business')


class DeleteFormBusiness(FlaskForm):
    business_id = StringField('Business ID',
                              validators=[DataRequired(), Length(min=2, max=4)])

    submit = SubmitField('Delete Business')


class UpdateFormBusiness(FlaskForm):
    business_id = StringField('Business ID',
                              validators=[DataRequired(), Length(min=2, max=4)])

    address = StringField('Address',
                          validators=[DataRequired(), Length(min=2, max=45)])

    founding_date = StringField('Founding Date',
                                validators=[DataRequired(), Length(min=2, max=25)])

    business_name = StringField('Business Name',
                                validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Update Business')


class AddFormAnalyst(FlaskForm):
    analyst_id_number = StringField('Analyst ID Number',
                                    validators=[DataRequired(), Length(min=2, max=4)])

    stock_id = StringField('Stock ID',
                           validators=[DataRequired(), Length(min=2, max=12)])

    analyst_name = StringField('Name',
                               validators=[DataRequired(), Length(min=2, max=25)])

    analyst_company = StringField('Company',
                                  validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Add Analyst')


class DeleteFormAnalyst(FlaskForm):
    analyst_id_number = StringField('Analyst ID Number',
                                    validators=[DataRequired(), Length(min=2, max=4)])

    submit = SubmitField('Delete Analyst')


class UpdateFormAnalyst(FlaskForm):
    analyst_id_number = StringField('Analyst ID Number',
                                    validators=[DataRequired(), Length(min=2, max=4)])

    stock_id = StringField('Stock ID',
                           validators=[DataRequired(), Length(min=2, max=12)])

    analyst_name = StringField('Name',
                               validators=[DataRequired(), Length(min=2, max=25)])

    analyst_company = StringField('Company',
                                  validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Update Analyst')


class AddFormStock(FlaskForm):
    stock_id = StringField('Stock ID',
                           validators=[DataRequired(), Length(min=2, max=12)])

    company_id = StringField('Company ID',
                             validators=[DataRequired(), Length(min=2, max=4)])

    prediction_id = StringField('Prediction ID',
                                validators=[DataRequired(), Length(min=2, max=4)])

    predict_stock_price = IntegerField('Predict Stock Price',
                                       validators=[DataRequired()])

    strong_buy = SelectField('Strong Buy', choices=[(1, 1), (0, 0)])

    rating_buy = SelectField('Rating Buy', choices=[(1, 1), (0, 0)])

    rating_sell = SelectField('Rating Sell', choices=[(1, 1), (0, 0)])

    strong_sell = SelectField('Strong Sell', choices=[(1, 1), (0, 0)])

    rating_hold = SelectField('Rating Hold', choices=[(1, 1), (0, 0)])

    stock_price = IntegerField('Stock Price',
                               validators=[DataRequired()])

    sector = StringField('Sector',
                         validators=[DataRequired(), Length(min=2, max=255)])
    belongs_to = StringField('Belongs To Exchange(Name)',
                       validators=[DataRequired(), Length(min=2, max=25)])

    submit = SubmitField('Add Stock')


class DeleteFormStock(FlaskForm):
    stock_id = StringField('Stock ID',
                           validators=[DataRequired(), Length(min=2, max=12)])

    submit = SubmitField('Delete Stock')


class UpdateFormStock(FlaskForm):
    stock_id = StringField('Stock ID',
                           validators=[DataRequired(), Length(min=2, max=12)])

    company_id = StringField('Company ID',
                             validators=[DataRequired(), Length(min=2, max=4)])

    prediction_id = StringField('Prediction ID',
                                validators=[DataRequired(), Length(min=2, max=4)])

    predict_stock_price = IntegerField('Predict Stock Price',
                                       validators=[DataRequired()])

    strong_buy = SelectField('Strong Buy', choices=[(1, 1), (0, 0)])

    rating_buy = SelectField('Rating Buy', choices=[(1, 1), (0, 0)])

    rating_sell = SelectField('Rating Sell', choices=[(1, 1), (0, 0)])

    strong_sell = SelectField('Strong Sell', choices=[(1, 1), (0, 0)])

    rating_hold = SelectField('Rating Hold', choices=[(1, 1), (0, 0)])

    stock_price = IntegerField('Stock Price',
                               validators=[DataRequired()])

    sector = StringField('Sector',
                         validators=[DataRequired(), Length(min=2, max=255)])
    
    belongs_to = StringField('Belongs To Exchange(Name)',
                       validators=[DataRequired(), Length(min=2, max=25)])
    
    submit = SubmitField('Update Stock')


class DeleteFormStockWatchlist(FlaskForm):
    stock_id = StringField('Stock ID',
                           validators=[DataRequired(), Length(min=2, max=12)])

    submit = SubmitField('Delete Stock')
 
class PROAddFormOffering(FlaskForm):
    offeringID = StringField('Offering ID Number  ',
                                    validators=[DataRequired(), Length(min=2, max=4)])

    iD = StringField('Stock ID           ',
                           validators=[DataRequired(), Length(min=2, max=12)])

    offer_quant = IntegerField('Quantity of Stock  ',
                               validators=[DataRequired()])

    offer_price = IntegerField('Offer Price        ',
                               validators=[DataRequired()])

    statusComplete = SelectField('Status Complete',
                         choices=[("Yes", "Yes"), ("No", "No")])

    statusNotComplete = SelectField('Status Incomplete',
                         choices=[("Yes", "Yes"), ("No", "No")])


    submit = SubmitField('Add Offering')

class PROUpdateFormOffering(FlaskForm):
        offeringID = StringField('Offering ID Number',
                                    validators=[DataRequired(), Length(min=2, max=4)])


        statusComplete = SelectField('Status Complete',
                         choices=[("Yes", "Yes"), ("No", "No")])

        statusNotComplete = StringField('Status Incomplete',
                         choices=[("Yes", "Yes"), ("No", "No")])


        submit = SubmitField('Update Offering')

class PRODeleteFormOffering(FlaskForm):
    offerID = StringField('Offer ID',
                           validators=[DataRequired(), Length(min=1, max=4)])

    submit = SubmitField('Delete Offering')
