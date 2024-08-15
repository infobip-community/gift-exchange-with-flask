import sqlite3
from flask import Flask, render_template, request, flash

app = Flask(__name__)

app.secret_key = "secret key"

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'GET':
       pass
   else:
       name = request.form.get('name')
       number = request.form.get('number')
       if not all((name, number)):
           flash("Please enter both a name and a phone number.")
       else:
           print(f"You clicked the button with name {name} and number {number}!")
           add_new_person_to_db(name, number)
           flash(f"You added {name} with number {number}!")
   return render_template('app.html')


def add_new_person_to_db(name, number):
   conn = sqlite3.connect('database.db')
   cur = conn.cursor()
   cur.execute(f"""
      INSERT INTO people (name, phone_number) VALUES
         ('{name}', '{number}')"""
         )
   conn.commit()
   conn.close()