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

app.run(debug=True) 
@app.route('/searchUser')
def searchUser():
    reslt_search=request.args.get('search')
    values=reslt_search
    sql=f" SELECT * from maindb.users_table where concat(firstname,lastname,email,phonenumber,address) like'%{values}%';"
    newcursor.execute(sql)
    searchResult=newcursor.fetchall()
    
    if request.args.get('page')!=None:

        current_page= int(request.args.get('page'))-1
    else:
        current_page=0

    sql="SELECT * FROM users_table order by user_id desc limit %s,2"
    values = (current_page,)
    newcursor.execute(sql,values)
    details = newcursor.fetchall()
    newcursor.execute("SELECT count(*) total_rec FROM maindb.users_table")
    page = newcursor.fetchone()
    total_pages=int(page['total_rec']/2)  # no of items per page
    return render_template("search_user.html",total_pages=total_pages,current_page=current_page,searchResult=searchResult)  

@app.route('/')
def index():
    
    
    if request.args.get('page')!=None:

        current_page= int(request.args.get('page'))-1
    else:
        current_page=0

    sql="SELECT * FROM users_table order by user_id desc limit %s,2"
    values = (current_page,)
    newcursor.execute(sql,values)
    details = newcursor.fetchall()
    newcursor.execute("SELECT count(*) total_rec FROM maindb.users_table")
    page = newcursor.fetchone()
    total_pages=int(page['total_rec']/2)  # no of items per page
    return render_template("index.html",details=details,total_pages=total_pages,current_page=current_page)

@app.route('/add_details',methods=['GET','POST'])
def add_details():

    if request.method == 'POST':
        firstname = escape (request.form['FirstName'])
        lastname = escape(request.form['LastName'])
        age = escape(request.form['Age']) 
        email = escape (request.form['Email'])
        phonenumber = escape(request.form['PhoneNumber'])
        address = escape(request.form['Address'])
        userroles = escape(request.form['UserRoles'])
        password = escape(request.form['Password'])


        sql=""" INSERT INTO users_table(firstname,lastname,age,email,phonenumber,address,userroles,password)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        values=(firstname,lastname,int(age),email,int(phonenumber),address,userroles,password)

        newcursor.execute(sql,values)
        condb.commit()

        return redirect(url_for('index'))

    return render_template('submit.html')


