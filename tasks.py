from microsoftbotframework import Response
import celery
import requests
import json
import smtplib

def echo_response(message):
    if message["type"] == "message":
        response = Response(message)

        if "kids" in message["text"]:
            r = requests.get('https://api.suncorp.com.au/olo/v1/interestRate/api/v1/products/kidsa')
            product = r.json()
            response.reply_to_activity('Yes, surely! We have a {}.'.format(product['name']))
            return

        if "bonus" in message["text"]:
            r = requests.get('https://api.suncorp.com.au/olo/v1/interestRate/api/v1/products/kidsa')
            product = r.json()
            response.reply_to_activity(product['description'])
            return

        if "interest" in message["text"]:
            r = requests.get('https://api.suncorp.com.au/olo/v1/interestRate/api/v1/products/kidsa')
            product = r.json()
            interest = product['data'][1]['values'][0]
            bonus = product['data'][2]['values'][0]
            response.reply_to_activity('The interest rate is ' + interest)
            response.reply_to_activity('There\'s also a bonus interest of ' + bonus)
            return

        if "home loan" in message["text"]:
            r = requests.get('https://api.suncorp.com.au/olo/v1/interestRate/api/v1/products/fixhome')
            message_response = r.json()
            response_info = response.reply_to_activity(message_response['name'])
            return

        if "hello" in message["text"]:
            response.reply_to_activity('Hello! Bob the Banker at your service. How can I help you?')
            return

        sender = 'bobthebanker@suncorp.com.au'
        receivers = ['andrea.vincita@suncorp.com.au']

        message = """From: Bob the Banker <bobthebanker@suncorp.com.au>
        To: Call Center <callcenter@suncorp.com.au>
        Subject: Customer Query from Bot Chat

        Hello,\n
        There's customer asking a question that I can't answer. \n
        Can you please get in touch with them please? Here is their question: \n {}
        """.format(message["text"])

        try:
           smtpObj = smtplib.SMTP('smlsmtp.suncorpmetway.net', 25)
           smtpObj.sendmail(sender, receivers, message)
           response.reply_to_activity('Thanks for your question, I am currently not able to answer it yet but I have forwarded your query to our friendly Customer Service staffs. Rest assured.')
           print ("Successfully sent email")
        except SMTPException:
           print ("Error: unable to send email")
