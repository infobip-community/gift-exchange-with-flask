from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'GET':
       pass
   else:
       name = request.form.get('name')
       number = request.form.get('number')
       print(f'you clicked the button with name {name} and number {number}!')
   return render_template('app.html')