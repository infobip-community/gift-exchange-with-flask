import sqlite3
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash
from infobip_channels.sms.channel import SMSChannel

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv('IB_API_KEY')
tfa_application_id = os.getenv('TFA_APP_ID')
tfa_template_id = os.getenv('TFA_TEMPLATE_ID')

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
           send_verification_text(number)
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

def send_verification_text(number):
    channel = SMSChannel.from_env()
    response = channel.send_pin_over_sms(
        {"ncNeeded": "false"},
        {
            "applicationId": tfa_application_id,
            "messageId": tfa_template_id,
            "from": "InfoSMS",
            "to": number,
        }
    )
    save_pin_id_for_number(number, response.pin_id)


def save_pin_id_for_number(number, pin_id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"""
        UPDATE people
        SET verification_code = '{pin_id}'
        WHERE phone_number = {number};"""
    )
    conn.commit()
    conn.close()

@app.route('/verify', methods=['GET', 'POST'])
def verify():
   if request.method == 'GET':
       pass
   else:
       name = request.form.get('name')
       number = request.form.get('number')
       pin = request.form.get('pin')
       if not all((name, number, pin)):
           flash("Please enter all required details.")
       else:
           print(f"You clicked the button with name {name}, number {number} and PIN {pin}!")
           verify_number(name, number, pin)
   return render_template('verify.html')

def verify_number(name, number, pin):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(f"""SELECT verification_code from people
                WHERE name = '{name}' AND phone_number = {number}""")
    pin_id = cur.fetchone()[0]
    channel = SMSChannel.from_env()
    response = channel.verify_phone_number(
        pin_id,
        {"pin": f"{pin}"}
    )
    if response.verified:
        cur.execute(f"""
            UPDATE people
            SET verified = 1
            WHERE phone_number = {number};"""
        )
        conn.commit()
        flash(f"Your number has been verified!")
    else:
        flash(f"Error: Number not verified: {response.pin_error}")
    conn.close()