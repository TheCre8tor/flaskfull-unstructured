from flask import Flask, render_template, make_response, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import pymysql

# Local Modules
from oi_form import LoginForm  # I import this module from my form.py


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jahd782882ndjdj'  # For CSRF protection


# Database Connection -->
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional

pymysql.install_as_MySQLdb()  # FIX: Error No module named MySQLdb

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


# Database Model -->
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(120))
    password = db.Column(db.String(100))

    # Constructor -->
    def __init__(self, username, email, address, password):
        self.username = username
        self.email = email
        self.address = address
        self.password = password

# db.create_all()  # Run this once to initialize database.

# -- Adding new data to the database -->
# data = UserInfo('Oredola street', '0908766')
# db.session.update(data) 
# db.session.commit()


# NOTE:
# 1. Cookies are used for storing user information in the browser


# VIEW ROUTES -->
@app.route('/')
def Home():
    return render_template('index.html')


@app.route('/<string:name>')
def html_pages(name):
    try:
        if name == 'index':
            return redirect('/')
        return render_template(f'{name}.html')
    except:
        return page_not_found(name)


# LOGIN VIEW FUNCTION -->
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        if request.form['username'] != 'alexander' and request.form['password'] != '123456':
            flash('Incorrect Username and Password, Please Try Again')
        elif request.form['username'] != 'alexander':
            flash('Incorrect Username, Please Try Again')
        elif request.form['password'] != '123456':
            flash('Incorrect Password, Please Try Again')
        else:
            return redirect(url_for('Home'))

    return render_template('login.html', title='Login', form=form)


# ERROR HANDLING -->
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


# SETTING AND GETTING COOKIES -->
@app.route('/set')
def set_cookie():
    response = make_response('I have set the cookie')
    response.set_cookie('myapp', 'Flask Web Development')

    return response


@app.route('/get')
def get_cookie():
    myapp = request.cookies.get('myapp')
    return f'Cookie Content Is {myapp}'


# SERVER -->
if __name__ == "__main__":
    # app.run(debug=True)  # We need to comment this out to allow manager to run
    manager.run()
