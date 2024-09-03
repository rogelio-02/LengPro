import pymysql
from app import app
from dbconfig import mysql
#from tables import Results
from flask import flash, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash

#app = Flask(__name__)
#app.debug = True

@app.route('/')
def helloworld():
    return render_template("frm.html") 
    
@app.route('/show', methods = ["POST","GET"])
def show():
    conn = None
    cursor = None
    try:
        if request.method == "POST":
           nf = request.form['fn']
           nl = request.form['ln']
           print ("el nombre ", nf, " ", nl)
           conn = mysql.connect()
           cursor = conn.cursor(pymysql.cursors.DictCursor)
           #sql = "insert into empleados(name, lname) values('%s', '%s')"
           #sql = "DELETE FROM empleados WHERE name =  "VALOR"
           
           values = ( nf, nl,)

           #cursor.execute(sql, values)
           #conn.commit()
           cursor.execute("SELECT * FROM  empleados")
           rows = cursor.fetchall()
           print (rows)
           return render_template("out.html", f=nf, l=nl, productos = rows)
    except Exception as e:
       print(e)
    finally:
       cursor.close() 
       conn.close()       


if __name__ == '__main__':
    app.run()