from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flaskext.mysql import MySQL

from flask_table import Table, Col

app = Flask(__name__)

mysql = MySQL()
 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root1234@localhost:3306/hospitaldb'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root@1234'
app.config['MYSQL_DATABASE_DB'] = 'hospitaldb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306


mysql.init_app(app)


class hospital_employee(Table):
    empid = Col('ID')
    empname = Col('Name')
    empsurname = Col('Surname')
    contactno = Col('Contact')
    speciality = Col('Speciality')
    salary = Col('Salary')
    dateofjoining = Col('DateOfjoining')
    shift = Col('Shift')
    email = Col('Email')







@app.route("/xcxc")
def index():
    rows = [(1, 'Govind', 'Sharma', 8085, 'ENT', 85000, 2014, 4, 7, 0, 0, 'Morning', 'sharmagovind92@gmail.com'),(4, 'Rohan', 'Kundra', 5456465, 'Ear', 434343, 2003, 2, 12, 2, 1, 'Morning', 'gfdfsdtst@gmail.com')]
    # return "fdfdgff"
    return render_template("user.html", rows=rows)

@app.route("/employees", methods=["GET"])
def getdata():

    if request.method == "GET":
        try:
            db = "hospital_employees"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospital_employees")
            rows = cursor.fetchall()
            for item in rows:
                print (item)
            conn.commit()
            conn.close()
            return render_template('user.html', db=db, rows=rows)
        except Exception as e:
            df = {
                "Error_Message" : "Something went wrong in GET request with id ",
                "Error" : e
            }
        
            return df

    
    
    
@app.route("/employee/<int:id>")
def getdatawithid(id):
    db = "hospital_employees"
    try:
        if request.method == "GET" and id != None:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospitaldb.hospital_employees where empid = %s", id)
            rows = cursor.fetchone()
            print("Data :- ", rows)
            conn.commit()
            conn.close()
            return render_template('user.html', db=db, rows=rows)
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in GET request with id ",
            "Error" : e
        }
        print("Error in GET with id in employee", e)
        return df
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug= True)
    # app.run(debug=True)