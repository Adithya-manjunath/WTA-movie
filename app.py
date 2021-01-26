import requests
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 

app=Flask(__name__)

app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'geeklogin'
  
mysql = MySQL(app) 
  
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/basicinfo", methods =['GET', 'POST'])
def basicinfo():
    return render_template("basicinfo.html",data=data,data2=data2,data3=data3)

@app.route("/userreviews", methods =['GET', 'POST'])
def userreviews():
    return render_template("userreviews.html",data=data,data2=data2,data3=data3)

@app.route("/parentalguide", methods =['GET', 'POST'])
def parentalguide():
    return render_template("parentalguide.html",data=data,data2=data2,data3=data3)

@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg) 
  
@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 
  
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, )) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)




@app.route("/search",methods=["POST"])
def search():
    name=request.form.get("name")
    url1 = "https://imdb8.p.rapidapi.com/title/find"

    url = "https://imdb8.p.rapidapi.com/title/get-parental-guide"

    url2 = "https://imdb8.p.rapidapi.com/title/get-user-reviews"

    querystring = {"q":name}

    headers = {
    'x-rapidapi-key': "f35a0aa3ebmsh7fea6555978f85cp1290b4jsne7fb284903a7",
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    response = requests.request("GET", url1, headers=headers, params=querystring)
    global data
    global data2
    global data3
    data = response.json()
    print(type(data))
    pprint(data['query'])
    
    querystring1 = {"tconst":data["results"][0]["id"][7:-1]}
    response2 = requests.request("GET", url, headers=headers, params=querystring1)
    response3 = requests.request("GET", url2, headers=headers, params=querystring1)
    data2 = response2.json()
    data3 = response3.json()
    print(data2)
    print(data3)
    return render_template("basicinfo.html",data=data,data2=data2,data3=data3)

    

if __name__ == "__main__":
    app.run(debug=True)





