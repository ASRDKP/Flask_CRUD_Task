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
    

# class hospital_patient(Table):
    




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
        


@app.route("/addemp", methods=["GET","POST"])
def addemp():
    try:
        title = "Enter"
        if request.method == "POST":
            print("Inside Add Emp POST request")
            
            empname = request.form['empname']
            empsurname = request.form['empsurname']
            contactno = request.form['contactno']
            speciality = request.form['speciality']
            salary = request.form['salary']
            dateofjoining = request.form['dateofjoining']
            shift = request.form['shift']
            email = request.form['email']
            
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "INSERT INTO hospitaldb.hospital_employees(empname,empsurname,contactno,speciality,salary,dateofjoining,shift,email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (empname, empsurname, contactno, speciality, salary, dateofjoining, shift, email)
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
            
            return redirect('/employees')
        return render_template('employee.html', title=title)
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in addemp ",
            "Error" : e
        }
        
        print("Error: ", e)
        return df
    
@app.route('/update_emp', methods=['GET','PUT'])
def update_emp():
    try:
        title = "Update"
        if request.method == 'PUT':
            print("Inside update_emp method")
            
            empid = request.form['empid']
            empname = request.form['empname']
            empsurname = request.form['empsurname']
            contactno = request.form['contactno']
            speciality = request.form['speciality']
            salary = request.form['salary']
            dateofjoining = request.form['dateofjoining']
            shift = request.form['shift']
            email = request.form['email']
        
            
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "Update hospitaldb.hospital_employees SET empname = %s, empsurname = %s, contactno = %s, speciality = %s, salary = %s, dateofjoining = %s, shift = %s, email = %s WHERE empid = %s"
            data = (empname, empsurname, contactno, speciality, salary, dateofjoining, shift, email, empid)
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
            
            return redirect('/employees')
        
        return render_template('addemployee.html', title=title)
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in update_emp",
            "Error" : e
        }
        
        print("Error", e)

        return df
    
@app.route('/delete_emp/<int:id>', methods=['DELETE'])
def delete_emp(id):
    try:
        if request.method == 'DELETE':
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "DELETE FROM hospitaldb.hospital_employees WHERE empid = %s"
            data = (id)
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
            return redirect('/employees')
        
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in Delete_emp ",
            "Error" : e
        }
        print("Error: ", e)
        
        return df
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug= True)
    # app.run(debug=True)