from flask import Flask,render_template,url_for,request,redirect
from markupsafe import escape
import mysql.connector

condb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='2234035mgr',
    database='maindb'
)

newcursor=condb.cursor(dictionary=True)

app= Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add_details',methods=['GET','POST'])
def add_details():

    if request.method=='POST':
        firstname=escape (request.form['FirstName'])
        lastname=escape(request.form['LastName'])
        age=escape(request.form['Age']) 
        email=escape (request.form['Email'])
        phonenumber=escape(request.form['PhoneNumber'])
        address=escape(request.form['Address'])
        userroles=escape(request.form['UserRoles'])
        password=escape(request.form['Password'])


        sql=""" INSERT INTO users_table(firstname,lastname,age,email,phonenumber,address,userroles,password)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        values=(firstname,lastname,int(age),email,int(phonenumber),address,userroles,password)

        newcursor.execute(sql,values)
        condb.commit()

        return redirect(url_for('index'))

    return render_template('submit.html')



app.run(debug=True)    