from config.db import newcursor
class UserModel():
    def index(self,current_page):
        sql="SELECT * FROM users_table order by user_id desc limit %s,2"
        values = (current_page,)
        newcursor.execute(sql,values)
        users_list = newcursor.fetchall()
        newcursor.execute("SELECT count(*) total_rec FROM maindb.users_table")
        page = newcursor.fetchone()
        total_pages=int(page['total_rec']/2)  # no of items per page    

        return {"page":page,
                 "total_pages":total_pages,
                 "users_list": users_list  }