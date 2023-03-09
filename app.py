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
    

class patients_details(Table):
    patientsid = Col('ID')
    patientname = Col('Name')
    patientsurname = Col('Surname')
    disease = Col('Disease')
    undercareof = Col('Undercareof')
    emergencyContact = Col('EmergencyContact')
    dateofadmit = Col('DateOfAdmit')
    address = Col('Address')
    roomno = Col('Roomno')
    bedno = Col('Bedno')
    daysinhospital = Col('DaysInHOSPITAL')
    attendeeid = Col('AttendeeId')




@app.route("/employees", methods=["GET"])
def getempdata():

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
def getempdatawithid(id):
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
        


@app.route("/add_emp", methods=["GET","POST"])
def add_emp():
    try:
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
        return render_template('employee.html')
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in addemp ",
            "Error" : e
        }
        
        print("Error: ", e)
        return df
    
@app.route('/update_emp/<int:id>', methods=['GET','PUT'])
def update_emp(id):
    try:
        title = "Update"
        if request.method == 'PUT':
            print("Inside update_emp method")
            
            # empid = request.form['empid']
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
            data = (empname, empsurname, contactno, speciality, salary, dateofjoining, shift, email, id)
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
            
            return redirect('/employees')
        
        return render_template('updateemployee.html', title=title)
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in update_emp",
            "Error" : e
        }
        
        print("Error", e)

        return df
    
@app.route('/delete_emp', methods=['GET','DELETE'])
def delete_emp():
    try:
        if request.method == 'DELETE':
            empid = request.form['empid']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "DELETE FROM hospitaldb.hospital_employees WHERE empid = %s"
            cursor.execute(sql, empid)
            conn.commit()
            conn.close()
            return redirect('/employees')
        return render_template('delete_emp.html')
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in Delete_emp ",
            "Error" : e
        }
        print("Error: ", e)
        
        return df
    
    





@app.route("/patients", methods=["GET"])
def getpatientsdata():
    if request.method == "GET": 
        try:
            db = "patients_details"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients_details")
            rows = cursor.fetchall()
            for item in rows:
                print (item)
            print("@@@@")
            conn.commit()
            conn.close()
            return render_template('user.html', db=db, rows=rows)
        except Exception as e:
            df = {
                "Error" : "Something went wrong in Get_Patients Method",
                "Error_Message" : e
            }
        
        print("Error_Message: ", e)
        
        return df
    
    

@app.route("/patient/<int:id>", methods=["GET"])
def getpatientsdatawithid(id):
    if request.method == "GET": 
        try:
            db = "patients_details"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients_details where patientsid = %s", id)
            rows = cursor.fetchall()
            print("Patients Datawithid: ", rows)
            conn.commit()
            conn.close()
            return render_template('user.html', db=db, rows=rows)
        except Exception as e:
            df = {
                "Error" : "Something went wrong in Get_Patients Method",
                "Error_Message" : e
            }
        
        print("Error_Message: ", e)
        
        return df



@app.route("/add_patients", methods=["GET", "POST"])
def add_patient():
    try:
        if request.method == "POST":
            
            patientname = request.form['patientname']
            patientsurname = request.form['patientsurname']
            disease = request.form['disease']
            undercareof = request.form['undercareof']
            emergencyContact = request.form['emergencyContact']
            dateofadmit = request.form['dateofadmit']
            address = request.form['address']
            roomno = request.form['roomno']
            bedno = request.form['bedno']
            daysinhospital = request.form['daysinhospital']
            attendeeid = request.form['attendeeid']
            
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "INSERT INTO hospitaldb.patients_details(patientname,patientsurname,disease, undercareof, emergencyContact, dateofadmit, address, roomno, bedno, daysinhospital, attendeeid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (patientname, patientsurname, disease, undercareof, emergencyContact, dateofadmit, address, roomno, bedno, daysinhospital, attendeeid)
            cursor.execute(sql, data)
            conn.commit()
            conn.close()
            
            
            return redirect("/patients")
        return render_template('add_patient.html')
    except Exception as e:
        df = {
            "Error" : "Something went wrong in Get_Patients Method",
            "Error_Message" : e
        }
    
    print("Error_Message: ", e)
    
    return df


   
@app.route('/delete_patient', methods=['GET','DELETE'])
def delete_patient():
    try:
        if request.method == 'DELETE':
            patientsid = request.form['patientsid']
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "DELETE FROM hospitaldb.hospital_employees WHERE patientsid = %s"
            cursor.execute(sql, patientsid)
            conn.commit()
            conn.close()
            return redirect('/employees')
        return render_template('delete_patient.html')
    except Exception as e:
        df = {
            "Error_Message" : "Something went wrong in delete_patient ",
            "Error" : e
        }
        print("Error: ", e)
        
        return df
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug= True)
    # app.run(debug=True)