def searchUser():
    reslt_search=request.args.get('search')
    values=reslt_search
    sql=f" SELECT * from maindb.users_table where concat(firstname,lastname,email,phonenumber,address) like'%{values}%';"
    newcursor.execute(sql)
    return newcursor.fetchall()