from flask import Flask, jsonify
import sys
import pywhatkit
from datetime import datetime
import smtplib
import mysql.connector
import re
import pandas as pd

conn = mysql.connector.connect(host = "localhost", user = "root",passwd = "Immithun2605@", database = "detail")
curr = conn.cursor()
curr.execute("drop table customers")
#curr.execute("delete from customers")
curr.execute("""create table customers( id INT AUTO_INCREMENT PRIMARY KEY,name varchar(20) not null,mail varchar(30) unique not null, mobile varchar(10) unique not null, subscription varchar(10) not null)""")
conn.commit()
df = pd.read_excel(r"C:\Users\mithu\OneDrive\Desktop\python programs\details.xlsx",engine="openpyxl")
columns  = df.columns
columns  = columns[1::]
length = len(df[columns[0]])

start = "9876"
for x in range(length):
    name1,mail1,phno1,sub1 = "","","",""
    for y in columns:
        if(y=="mobile"):
            k = str(df[y].iloc[x])
            if(len(k)==10 and k[0] in start):
                phno1 = str(df[y].iloc[x])
        elif(y=="mail"):
            mail1 = df[y].iloc[x]
        elif(y=="Name"):
            name1 = df[y].iloc[x]
        elif(y=="subscription"):
            sub1 = df[y].iloc[x]
    query = "insert into customers(name,mail,mobile,subscription) values(%s,%s,%s,%s)"
    curr.execute(query,(name1,mail1,phno1,sub1))
    
curr.execute("select * from customers");
l = []
for x in curr.fetchall():
    l.append(x)
conn.commit()
def trigger_api():
    app = Flask(__name__)

    @app.route('/api/hello', methods=['GET'])
    def hello():
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("2112100@nec.edu.in", "dqv5tam6528")
        curr.execute("select name,mail,mobile,subscription from customers")
        list = []
        for x in curr.fetchall():
            k = x[1]
            message = "Welcome "+x[0]
            subs = x[3]
            p = str(x[2])
            if(subs=="mail"):
                if(re.match(r'^\S+@\S+\.\S+$',k)):
                    s.sendmail("2112100@nec.edu.in",k,message);
                print("Email sent successfully ",k);
                list.append("Email sent successfully "+k)
                
            elif(subs=="whatsapp"):
                if(len(p)==10 and p[0] in start):
                    cur = datetime.now()
                    h = cur.hour
                    m = cur.minute+1
                    if(m>57):
                        h+=1
                        m=1
                    if(p[0]!="+"):
                        p =  "+91"+p
                    pywhatkit.sendwhatmsg(p,message,h,m)
                print("Whatsapp message sent successfully ",p);
                list.append("Whatsapp message sent successfully  "+p)
        return jsonify(l,list)
    
    if __name__ == '__main__':
        app.run(debug=True)
trigger_api()
