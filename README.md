# **Co-ordinating a gift exchange with Flask and Infobip**

A web app which allows users to register for a gift exchange, assigns gifting relationships, and notifies users when the exchange can take place.

Source code for web app made with Flask and the [Infobip Python SDK](https://github.com/infobip-community/infobip-api-python-sdk).

## Pre-requisites

- Flask
- An Infobip account

## Running the project

Clone the repo

```
git clone https://github.com/infobip-community/gift-exchange-with-flask
```

Go to its directory:

```
cd ./gift-exchange-with-flask
```

Run the app:

```
flask run
```

## Following along

Each step of this guide is its own blog post and [a branch in this repo](https://github.com/infobip-community/gift-exchange-with-flask/branches):

- [Part 1](https://www.infobip.com/developers/blog/co-ordinating-a-gift-exchange-with-flask-and-infobip-part-1) covers building an app where users can enter their names and phone numbers, and the code is in [step-1](https://github.com/infobip-community/gift-exchange-with-flask/tree/step-1).
- [Part 2](https://www.infobip.com/developers/blog/co-ordinating-a-gift-exchange-with-flask-and-infobip-part-2) covers adding a database to the app to store the participant’s names and phone numbers, and the code is in [step-2](https://github.com/infobip-community/gift-exchange-with-flask/tree/step-2).
- Part 3 covers adding verification for users’ phone numbers, using Infobip’s 2-factor authentication API, and the code is in [step-3](https://github.com/infobip-community/gift-exchange-with-flask/tree/step-3).
- Part 4 covers adding a button to start the app and a new page to declare that the gift exchange is now active. This sends a text to everyone with their giftee’s name, and the code is in [step-4](https://github.com/infobip-community/gift-exchange-with-flask/tree/step-4).
- Part 5 covers creating a confirmation page once a partipant has bought their gift. After all the partcipants have bought their gifts, they will receive an text on their to inform them that they can now organise the actual gifting part, and the code is in step-5.
