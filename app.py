from flask import Flask,render_template,url_for,request,redirect,session,jsonify,flash
from markupsafe import escape
import mysql.connector
from models.userModel import UserModel
from config.db import newcursor,condb
import hashlib



app= Flask(__name__)
app.run(debug=True) 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login',methods=['GET','POST'])
def login():
    
    
    if request.method == 'POST':
        username = escape (request.form['username'])
        inputPassword = escape (request.form['password'])
        password = hashlib.sha256( inputPassword.encode('utf-8')).hexdigest()
        sql ="SELECT firstname,userroles FROM maindb.users_table WHERE email=%s AND password=%s ";
        values = (username,password)
        newcursor.execute(sql,values)
        name = newcursor.fetchone()
        if newcursor.rowcount > 0:
            username=name['firstname']
            userrole=name['userroles']
        
            session["username"] = username
            session["userrole"] = userrole
            flash("login succuss")
            return redirect(url_for('dashboard'))
        else:
            flash("invalid usernmae or password")

    return render_template("firstview/login.html")


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
        return render_template("users/index.html",users_list = searchNoneEmptyvalues["users_list"],total_pages = searchNoneEmptyvalues["total_pages"],current_page = current_page)   
        
    elif request.args.get("search") != None:
        if request.args.get('page')!= None:
            current_page = int(request.args.get('page'))-1     
        else:
            current_page = 0
        result_search = request.args.get('search')
        objectOne = UserModel()
        searchWithvalues = objectOne.withSearch(result_search, current_page)
        return render_template("firstview/index.html",users_list = searchWithvalues["users_list"],total_pages = searchWithvalues["total_pages"],current_page = current_page,result_search = result_search) 


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
        if newcursor.rowcount > 0:
            message='Data added succussfuly'
        else:
            None
        flash(message)        


        return redirect(url_for('users'))
    else:

        return render_template('users/addUserdetails.html')


@app.route('/user/edit/<int:user_id>',methods = ['GET','POST'])
def editUser(user_id):
    
    if request.method == 'GET':
        id = user_id
        objectone = UserModel()
        form = objectone.edituserdetails(id)
        return render_template("users/editUserdetail.html",form = form)
    if request.method == 'POST':
        firstname = escape (request.form['FirstName'])
        lastname = escape(request.form['LastName'])
        age = escape(request.form['Age']) 
        email = escape (request.form['Email'])
        phonenumber = escape(request.form['PhoneNumber'])
        address = escape(request.form['Address'])
        userroles = escape(request.form['UserRoles'])
        sql="UPDATE maindb.users_table SET firstname = %s,lastname = %s,age = %s, email = %s,phonenumber = %s,address = %s,userroles = %s WHERE user_id = %s"  
        values=(firstname,lastname,age,email,phonenumber,address,userroles,user_id) 
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
def logout():   
    session.pop('username','userrole')
    return redirect(url_for('index'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    
    
    return render_template('firstview/dashboard.html')

@app.route('/api/products',methods=['GET','POST'])
def api_products():
    sql="SELECT id,products,prize,stock FROM maindb.products"
    newcursor.execute(sql)
    product_details=newcursor.fetchall()

    return jsonify(product_details)

@app.route('/products',methods=['GET','POST'])
def products():
    return render_template('products/list.html')    

@app.route('/user/edit/password',methods = ['POST'])
def editPassword():
    if request.method == 'POST':   
        edit_password = request.form["password"]
        password = hashlib.sha256(edit_password.encode('utf-8')).hexdigest()
        user_id = request.form["id"]
        object_one = UserModel()
        object_one.edit_password(password,user_id)
        return jsonify("password changed")    
    return jsonify("something went wrong")
@app.route('/billing',methods=['GET','POST'])
def billing():
    return 0




        

      
 
    
                    