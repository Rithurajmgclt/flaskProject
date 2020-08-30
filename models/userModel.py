

from config.db import newcursor,condb
class UserModel():
    def employee_search(self,current_page):
        sql="SELECT * FROM users_table ORDER BY user_id desc LIMIT %s,2"
        values = (current_page,)
        newcursor.execute(sql,values)
        users_list = newcursor.fetchall()
        newcursor.execute("SELECT count(*) total_rec FROM maindb.users_table")
        page = newcursor.fetchone()
        total_pages=int(page['total_rec']/2)  # no of items per page    

        return {"page":page,
                 "total_pages":total_pages,
                 "users_list": users_list  }
    def user_pageination_withsearh(self, result_search, current_page):
        sql=f" SELECT * FROM maindb.users_table WHERE concat(firstname,lastname,email,phonenumber,address) like '%{result_search}%' limit {current_page},2;"
        newcursor.execute(sql)
        users_list = newcursor.fetchall() 
        sql=f"SELECT count(*) as total_rec FROM  maindb.users_table WHERE concat(firstname,lastname,email,phonenumber,address) like'%{result_search}%';"
        newcursor.execute(sql)
        page = newcursor.fetchone()
        total_pages= int(page['total_rec']/2)  # no of items per page  
        return {"page":page,
                 "total_pages":total_pages,
                 "users_list": users_list  }

    def edit_userdetails(self,id):
        sql="SELECT user_id,firstname,lastname,email,phonenumber,address,userroles  FROM  maindb.users_table WHERE user_id='%s'"
        values=(id,)
        newcursor.execute(sql,values)
        user_editdetails = newcursor.fetchone()
        return user_editdetails
    
    def edit_password(self,password,user_id):

        sql="UPDATE maindb.users_table SET password = %s WHERE user_id = %s"  
        values=(password,user_id) 
        newcursor.execute(sql,values)
        condb.commit()
    