
from flask import Flask,jsonify,request
import sys
import mysql.connector
import re

conn = mysql.connector.connect(host = "localhost",user= "root",passwd  ="password",database = "detail")
curr = conn.cursor()


app = Flask(__name__)

@app.route('/createuser')
def create_user():
    name = request.args.get('name')
    mail =  request.args.get('mail')
    mobile =  request.args.get('mobile')
    subscription =  request.args.get('subscription')
    query1 = "insert into customers(name,mail,mobile,subscription) values(%s,%s,%s,%s)"
    values = (name,mail,mobile,subscription)
    curr.execute(query1,values)
    conn.commit()
    return jsonify("User created successfully")
#----------------------------------------------------------------------------------------------------------------

@app.route('/readallusers',methods = ['GET'])

def readallusers():
    query2 = "select * from customers"
    curr.execute(query2)
    allusers = curr.fetchall()
    if(len(allusers)!=0):
        return jsonify(allusers)
    else:
        return jsonify("No users in the database"),404
        

@app.route('/readuser/<int:userid>',methods = ['GET'])

def readuser(userid):
    query3 = "select * from customers where id = %s"
    curr.execute(query3,(userid,))
    user = curr.fetchone()
    if(user):
        return jsonify(user)
    else:
        return jsonify("User Id not exist"),404
#-----------------------------------------------------------------------------------------------------------------
@app.route('/updateuser/<int:userid>')
def updateuser(userid):
    name = request.args.get('name')
    mail =  request.args.get('mail')
    mobile =  request.args.get('mobile')
    subscription =  request.args.get('subscription')
    query = "UPDATE customers SET name = %s, mail = %s ,mobile = %s, subscription = %s WHERE id = %s"
    values = (name,mail,mobile,subscription,userid)
    curr.execute(query,values)
    conn.commit()
    return jsonify("User updated successfully")
#-----------------------------------------------------------------------------------------------------------------
    
@app.route('/deleteuser/<int:userid>')

def deleteuser(userid):
    query4 = "delete from customers where id = %s"
    res = curr.execute(query4,(userid,))
    if(res==None):
        return jsonify("User deleted successfully")
    else:
        return jsonify("Invalid user")
    
@app.route('/deleteallusers')

def deleteallusers():
    query5 = "delete from customers"
    res = curr.execute(query5)
    if(res==None):
        return jsonify("Users deleted successfully")
#----------------------------------------------------------------------------------------------------------------- 


if __name__ == '__main__':
    app.run(debug = True)
    
