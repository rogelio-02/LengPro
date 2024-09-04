from app import app
import pymysql

def getDBConnection():
    connection = pymysql.connect(
        host='127.0.0.1',         
        user='root',    
        password='apolo9404', 
        database='form'  
    )
    return connection