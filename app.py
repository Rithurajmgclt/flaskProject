from flask import Flask,render_template,url_for,request,redirect
from markupsafe import escape
import mysql.connector
from models.userModel import UserModel
from config.db import newcursor,condb
import hashlib

app= Flask(__name__)
app.run(debug=True) 

@app.route('/',methods=['GET','POST'])
def inex():
    
    """
    if request.methed == 'POST':
        username = escape (request.form['Usernmae'])
        inputPassword = escape (request.form['Password'])
        password=hashlib.md5(inputPassword.encode())
    """


    return render_template("newlogin.html")


@app.route('/users',methods=['GET','POST'])
def users():

    if request.args.get('page')!=None:
        current_page= int(request.args.get('page'))-1
    else:
        current_page=0
    
   
    # if search is none and empty this condition will execute
    if request.args.get("search") == None or not request.args.get("search") :
        objectOne = UserModel()  
        searchNoneEmptyvalues = objectOne.emptySearch(current_page)  
        return render_template("index.html",users_list = searchNoneEmptyvalues["users_list"],total_pages = searchNoneEmptyvalues["total_pages"],current_page = current_page)   
        
    elif request.args.get("search") != None:
        if request.args.get('page')!= None:
            current_page = int(request.args.get('page'))-1     
        else:
            current_page = 0
        result_search = request.args.get('search')
        objectOne = UserModel()
        searchWithvalues = objectOne.withSearch(result_search, current_page)
        return render_template("index.html",users_list = searchWithvalues["users_list"],total_pages = searchWithvalues["total_pages"],current_page = current_page,result_search = result_search) 


@app.route('/adddetails/',methods=['GET','POST'])
def addDetails():

    if request.method == 'POST':
        firstname = escape (request.form['FirstName'])
        lastname = escape(request.form['LastName'])
        age = escape(request.form['Age']) 
        email = escape (request.form['Email'])
        phonenumber = escape(request.form['PhoneNumber'])
        address = escape(request.form['Address'])
        userroles = escape(request.form['UserRoles'])
        inputPassword = escape (request.form['Password'])
        password = hashlib.sha256( inputPassword.encode('utf-8')).hexdigest()

        sql="INSERT INTO maindb.users_table(firstname,lastname,age,email,phonenumber,address,userroles,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"  
        values=(firstname,lastname,age,email,phonenumber,address,userroles,password) 
        newcursor.execute(sql,values)
        condb.commit()

        return redirect(url_for('users'))
    else:

        return render_template('addUserdetails.html')


@app.route('/user/edit/<int:user_id>',methods = ['GET','POST'])
def editUser(user_id):
    
    if request.method == 'GET':
        id = user_id
        objectone = UserModel()
        form = objectone.edituserdetails(id)
        return render_template("editUserdetail.html",form = form)
    if request.method == 'POST':
        firstname = escape (request.form['FirstName'])
        lastname = escape(request.form['LastName'])
        age = escape(request.form['Age']) 
        email = escape (request.form['Email'])
        phonenumber = escape(request.form['PhoneNumber'])
        address = escape(request.form['Address'])
        userroles = escape(request.form['UserRoles'])
        password = escape(request.form['Password'])
        sql="UPDATE maindb.users_table SET firstname = %s,lastname = %s,age = %s, email = %s,phonenumber = %s,address = %s,userroles = %s,password = %s WHERE user_id = %s"  
        values=(firstname,lastname,age,email,phonenumber,address,userroles,password,user_id) 
        newcursor.execute(sql,values)
        condb.commit()
        return redirect(url_for('users'))
@app.route('/user/delete/<int:user_id>')
def deleteUsers(user_id):
    id=user_id
    sql="DELETE FROM maindb.users_table WHERE user_id='%s'"
    values=(id,)
    newcursor.execute(sql,values)
    condb.commit()
    return redirect(url_for('users'))


        

      
 
    
                    