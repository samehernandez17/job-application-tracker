from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import database as db


app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)



#============================================================================================
#Companies
#============================================================================================
COMPANY_FIELDS = []
