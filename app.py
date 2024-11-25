from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'penyuka_celana',  
    'password': 'celanaterkeren2024',
    'host': 'localhost',
    'database': 'celana_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM celana')
    celana_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', celana=celana_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['celanajin']
        ukuran = request.form['S']
        harga = request.form['250.0000']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO celana (celanajeans, S, 250.000) VALUES (%s, %s, %s)', (nama, ukuran, harga))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        nama = request.form['celanapesta']
        ukuran = request.form['M']
        harga = request.form['50.000']
        
        cursor.execute('UPDATE celana SET nama = %s, ukuran = %s, harga = %s WHERE id = %s', (nama, ukuran, harga, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM celana WHERE id = %s', (id,))
    celana = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', celana=celana)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM celana WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
