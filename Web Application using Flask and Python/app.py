from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app=Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from customers")
    data=cur.fetchall()
    return render_template("index.html",datas=data)

@app.route("/edit_user/<string:uid>",methods=['POST','GET'])
def edit_user(uid):
    try:  
        if request.method=='POST':
            name=request.form['name']
            mobile=request.form['mobile']
            mail=request.form['mail']
            subscription=request.form['subscription']
            con=sql.connect("database.db")
            cur=con.cursor()
            cur.execute("update customers set NAME=?,MOBILE=?,MAIL=?,SUBSCRIPTION=? where ID=?",(name,mobile,mail,subscription,uid))
            con.commit()
            flash('User Updated','success')
            return redirect(url_for("index"))
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from customers where ID=?",(uid,))
        data=cur.fetchone()
        return render_template("edit_user.html",datas=data)
    except sql.IntegrityError:
        flash('Please check your Mobile or Mail because it is possessed by one of our customer...!','warning')
        return render_template("edit_user.html",datas=data)
        
    
@app.route("/delete_user/<string:uid>",methods=['GET'])
def delete_user(uid):
    con=sql.connect("database.db")
    cur=con.cursor()
    cur.execute("delete from customers where ID=?",(uid,))
    con.commit()
    flash('User Deleted','warning')
    return redirect(url_for("index"))


@app.route("/add_user",methods=['POST','GET'])
def add_user():
    try:
        if request.method=='POST':
            name=request.form['name']
            mobile=request.form['mobile']
            mail=request.form['mail']
            subscription=request.form['subscription']
            con=sql.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into customers(NAME,MAIL,MOBILE,SUBSCRIPTION) values (?,?,?,?)",(name,mobile,mail,subscription))
            con.commit()
            flash('User Added','success')
            return redirect(url_for("index"))
        return render_template("add_user.html")
    except sql.IntegrityError:
        flash('Please check your Mobile or Mail because it is possessed by one of our customer...!','warning')
        return render_template("add_user.html")
    
if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)