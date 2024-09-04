from flask import Flask, render_template, request, redirect, url_for
from app import app
from dbconfig import getDBConnection
import pymysql


@app.route('/', methods=["GET"])
def index():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT * FROM agenda")
        contactos = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        contactos = []
    finally:
        cursor.close()
        connection.close()

    return render_template('frm.html', contactos=contactos)

@app.route('/', methods=['POST'])
def submit():
    firstName = request.form['name']
    lastName = request.form['lname']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO agenda (nombre, apellido) VALUES (%s,%s)", (firstName, lastName))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))    


if __name__ == "__main__":
    app.run()