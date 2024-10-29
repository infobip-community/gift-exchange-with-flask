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

@app.route('/start', methods=['GET', 'POST'])
def start_exchange():
   if request.method == 'GET':
       pass
   else:
       assign_gifts()
       send_details()
   return render_template('start.html')

def assign_gifts():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT id FROM people")
    people = cur.fetchall()

    for index in range(len(people)):
        person_id = people[index][0]
        # Get the next person's ID and wrap around
        next_index = (index + 1) % len(people)
        giftee_id = people[next_index][0]

        cur.execute(f"""
            UPDATE people SET giftee = {giftee_id} WHERE id = {person_id}
        """)

    conn.commit()
    conn.close()

def send_details():
    conn = sqlite3.connect('database.db')
    channel = SMSChannel.from_env()

    cur = conn.cursor()

    cur.execute("""
        SELECT p1.phone_number, p2.name 
        FROM people p1
        JOIN people p2 ON p1.giftee = p2.id
    """)
    results = cur.fetchall()

    # Send a message to everyone with their giftee's name
    for result in results:
        buyer = result[0]
        giftee = result[1]
        text = f"You are buying a gift for {giftee}"
        sms_response = channel.send_sms_message({
            'messages': [{
                'from': 'Gift Exchange app',
                'text': text,
                'destinations': [{
                    'to': buyer
                }],
            }]
        })

    conn.close()

@app.route('/confirm', methods=['GET', 'POST'])
def confirm_gift():
   if request.method == 'GET':
       pass
   else:
        name = request.form.get('name')
        if not name:
           flash("Please enter your name.")
        else: 
            confirm_gift_bought(name)
            flash(f"Thanks for confirming! You'll receive a text when everyone else has done so.")
   return render_template('confirm.html')

def confirm_gift_bought(name):
    conn = sqlite3.connect('database.db')
    channel = SMSChannel.from_env()
    cur = conn.cursor()

    # Update the gift_bought field for the person to 1
    cur.execute(f"""
        UPDATE people
        SET gift_bought = 1
        WHERE name = '{name}';
    """)
    conn.commit()

    cur.execute("SELECT name, phone_number, gift_bought FROM people;")
    people = cur.fetchall()
    gifts_bought = 0

    for person in people:
        if person[2] == 1:  # Check if gift_bought is 1
            gifts_bought += 1

    if gifts_bought == len(people):
        print("Everyone bought their gift!")
        for person in people:
            phone_number = person[1]
            sms_response = channel.send_sms_message({
                'messages': [{
                    'from': 'Gift Exchange app',
                    'text': "Everyone bought their gift! Time to meet up and exchange!",
                    'destinations': [{
                        'to': phone_number
                    }],
                }]
            })

    conn.close()
