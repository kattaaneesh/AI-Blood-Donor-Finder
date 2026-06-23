from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS donors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood_group TEXT,
        phone TEXT,
        city TEXT,
        available TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        blood_group = request.form['blood_group']
        phone = request.form['phone']
        city = request.form['city']

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO donors
        (name,age,blood_group,phone,city,available)
        VALUES(?,?,?,?,?,?)
        """,(name,age,blood_group,phone,city,"Yes"))

        conn.commit()
        conn.close()

        return redirect('/donors')

    return render_template("register.html")

@app.route('/search', methods=['GET','POST'])
def search():

    results = []

    if request.method == 'POST':

        blood_group = request.form['blood_group']

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM donors
        WHERE blood_group=?
        """,(blood_group,))

        results = cur.fetchall()

        conn.close()

    return render_template("search.html", results=results)

@app.route('/donors')
def donors():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM donors")

    data = cur.fetchall()

    conn.close()

    return render_template("donors.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
