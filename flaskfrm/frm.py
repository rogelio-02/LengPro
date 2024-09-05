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

@app.route('/delete/<int:id>', methods=['POST'])
def delete_contact(id):
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM agenda WHERE idPersona = %s", (id,))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        firstName = request.form['name']
        lastName = request.form['lname']

        try:
            cursor.execute("UPDATE agenda SET nombre = %s, apellido = %s WHERE idPersona = %s", (firstName, lastName, id,))
            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('index'))
    
    else:
        try:
            cursor.execute("SELECT * FROM agenda WHERE idPersona = %s", (id,))
            contacto = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            contacto = None
        finally:
            cursor.close()
            connection.close()

        return render_template('out.html', contacto=contacto)


if __name__ == "__main__":
    app.run()
