from flask import Flask,render_template,url_for,request,redirect,session,jsonify,flash
from markupsafe import escape
import mysql.connector
from models.userModel import UserModel

from config.db import newcursor,condb
import hashlib



app= Flask(__name__)
app.run(debug=True) 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login',methods = ['GET','POST'])
def login():
    
    
    if request.method == 'POST':
        username = escape (request.form['username'])
        input_password = escape (request.form['password'])
        password = hashlib.sha256( input_password.encode('utf-8')).hexdigest()
        sql = 'SELECT firstname,userroles FROM maindb.users_table WHERE email=%s AND password=%s'
        values = (username,password)
        newcursor.execute(sql,values)
        name = newcursor.fetchone()
        condb.commit()
        if newcursor.rowcount >0:
            session["username"] = name['firstname']
            session["userrole"] = name['userroles']
            flash("login success","success")
            return redirect(url_for('dashboard'))

 
            
        else:
            flash('invalid usernmae or password','danger')
            return render_template("firstview/login.html")
    else:

        return render_template("firstview/login.html")

@app.route('/users',methods = ['GET','POST'])
def users():
    
    if 'username' in session and session['userrole'] == 'Manager':

    

        if request.args.get('page')!= None:
            current_page= int(request.args.get('page'))-1
       
        else:
            current_page=0
     
    
   
    # if search is none and empty this condition will execute
        if request.args.get("search") == None or not request.args.get('search') :
            object_one = UserModel()  
            searchnone_emptyvalues = object_one.employee_search(current_page)  
            return render_template("users/index.html",users_list = searchnone_emptyvalues["users_list"],total_pages = searchnone_emptyvalues["total_pages"],current_page = current_page)   
        
        elif request.args.get("search") != None:
            if request.args.get('page')!= None:
                current_page = int(request.args.get('page'))-1     
            else:
                current_page = 0
            result_search = request.args.get('search')
            object_one = User_model()
            search_withvalues = object_one.user_pageination_withsearh(result_search, current_page)
            return render_template("firstview/index.html",users_list = search_withvalues["users_list"],total_pages = search_withvalues["total_pages"],current_page = current_page,result_search = result_search) 
    else:
        return redirect(url_for('dashboard'))


@app.route('/adddetails/',methods=['GET','POST'])
def addDetails():
    if 'username' in session and session['userrole'] == "Manager":



        if request.method == 'POST':
            firstname = escape (request.form['FirstName'])
            lastname = escape(request.form['LastName'])
            age = escape(request.form['Age']) 
            email = escape (request.form['Email'])
            phonenumber = escape(request.form['PhoneNumber'])
            address = escape(request.form['Address'])
            userroles = escape(request.form['UserRoles'])
            input_password = escape (request.form['Password'])
            password = hashlib.sha256( input_password.encode('utf-8')).hexdigest()

            sql = "INSERT INTO maindb.users_table(firstname,lastname,age,email,phonenumber,address,userroles,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"  
            values = (firstname,lastname,age,email,phonenumber,address,userroles,password) 
            newcursor.execute(sql,values)
            condb.commit()
            if newcursor.rowcount > 0:
                message = 'Data added succussfuly'
            else:
                None
            flash(message)        


            return redirect(url_for('users'))
        else:

            return render_template('users/add_user_details.html')
    else:
        return redirect(url_for('dashboard'))
       


@app.route('/user/edit/<int:user_id>',methods = ['GET','POST'])
def editUser(user_id):

    if 'username' in session and session['userrole'] == 'Manager':
    
        if request.method == 'GET':
            id = user_id
            objectone = UserModel()
            form = objectone.edit_userdetails(id)
            return render_template("users/edit_user_edtails.html",form = form)
        if request.method == 'POST':
            firstname = escape (request.form['FirstName'])
            lastname = escape(request.form['LastName'])
            age = escape(request.form['Age']) 
            email = escape (request.form['Email'])
            phonenumber = escape(request.form['PhoneNumber'])
            address = escape(request.form['Address'])
            userroles = escape(request.form['UserRoles'])
            sql="UPDATE maindb.users_table SET firstname = %s,lastname = %s,age = %s, email = %s,phonenumber = %s,address = %s,userroles = %s WHERE user_id = %s"  
            values = (firstname,lastname,age,email,phonenumber,address,userroles,user_id) 
            newcursor.execute(sql,values)
            condb.commit()
            return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))

@app.route('/user/delete/<int:user_id>')
def delete_users(user_id):

    if 'username' in session and session['userrole'] == 'Manager':

        id=user_id
        sql = "DELETE FROM maindb.users_table WHERE user_id='%s'"
        values = (id,)
        newcursor.execute(sql,values)
        condb.commit()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))    

@app.route('/user/logout',methods = ['GET','POST'])   
def logout():
    session.pop('username','userrole')
    flash('you have been loged out','danger')  
    return redirect(url_for('login'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():

    if 'username' in session:
        return render_template('firstview/dashboard.html')
    else:
        return redirect(url_for('login')) 

@app.route('/api/products',methods = ['GET','POST'])
def api_products():
    if 'username' in session:
        if request.method == 'POST':
            offset_limit = int(request.form['offset_limit'])
            print(offset_limit)
            values = (offset_limit,)
            sql="SELECT id,product,prize,details FROM maindb.products ORDER BY id ASC LIMIT %s,6"
            newcursor.execute(sql,values)
            product_details=newcursor.fetchall()
            print(product_details)
            return jsonify(product_details)

        sql="SELECT id,product,prize,details FROM maindb.products LIMIT 0,6"
        newcursor.execute(sql)
        product_details=newcursor.fetchall()
    

        return jsonify(product_details)
    else:
        return redirect(url_for('login'))
@app.route('/products',methods = ['GET','POST'])
def products():
    if 'username' in session:
        return render_template('products/list.html')
    else:
        return redirect(url_for('dashboard'))       

@app.route('/user/edit/password',methods = ['POST'])
def editPassword():
    if 'username' in session and session['userrole'] == "Manager":
        if request.method == 'POST':   
            edit_password = request.form["password"]
            password = hashlib.sha256(edit_password.encode('utf-8')).hexdigest()
            user_id = request.form["id"]
            object_one = UserModel()
            object_one.edit_password(password,user_id)
            return jsonify("password changed")    
        return jsonify("something went wrong")
    else:
        return redirect(url_for('login'))

@app.route('/billing',methods = ['GET','POST'])
def billing():
    return 0
@app.route('/productdetails',methods = ['GET'])
def produtdetails():
   
    sql="SELECT id,product,prize,image,stock,details FROM maindb.products "
    newcursor.execute(sql)
    product_details = newcursor.fetchall()
    return render_template("products/product_details.html",product_details=product_details)




        

      
 
    
                    