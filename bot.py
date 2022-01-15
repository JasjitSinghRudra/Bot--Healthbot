from flask import Flask, request
# import requests
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector
from mysql.connector import Error
from random import randint
from time import sleep
from datetime import date
from PIL import Image

# Connection to Localhost
try:
    connection = mysql.connector.connect(host='localhost', database='hospital', user='root', password='')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

app = Flask(__name__)


@app.route('/mybot', methods=['POST'])
def mybot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    global flag, a, b, c, d, ref_flag
    red_flag = 1

    # For putting a nice appointment date, month and time
    today = date.today()
    d1 = today.strftime("%d")
    d2 = today.strftime("%m")
    d3 = today.strftime("%y")
    appointment_time = randint(1, 4)

    # For generating a random file id that will later help us in searching for records
    file_id = randint(100000, 999999)

    if incoming_msg == "cancel" or incoming_msg == "go back":
        msg.body("Your process has been cancelled. If there anything else I could do for you?")
        responded = True
        flag = 0

    if incoming_msg == "list of doctors" and flag == 0:
        msg.body("We have Dr. Phil with us today")
        responded = True

    if "book appointment" in incoming_msg or "see a doctor" in incoming_msg and flag == 0:
        msg.body(
            "Which department would you like to visit?\n\n1 - General Surgery\n2 - Internal Medicine\n3 - Gynaecology\n4 - Obstetrics\n5 - Ophthalmology\n6 - Orthopaedics\n7 - Dermatology Venereology & Leprology\n8 - ENT\n9 - Paediatric")
        flag += 1
        responded = True

    # General Surgery
    doctors = ['Dr. Gilbert Nightray', 'Dr. James Dee', 'Dr. Christopher Turk']
    doc = randint(0, 2)

    if incoming_msg == "1" or "general surgery" in incoming_msg and flag == 1:
        msg.body("Are you here for the first time or for follow-up?")
        flag += 1
        responded = True

    # Follow Up
    if "follow up" in incoming_msg or "i'm old" in incoming_msg and flag == 2:
        msg.body("Please enter your file reference id")
        responded = True
        ref_flag += 1

    if ref_flag == 1 and len(incoming_msg) == 6:
        mycursor = connection.cursor(buffered=True)
        finduser = ("SELECT * FROM search WHERE file_id = %s")
        mycursor.execute(finduser, [(incoming_msg)])
        results = mycursor.fetchall()
        connection.commit()
        if results:
            msg.body("Your appointment for follow up has been confirmed. Please visit our facility on " + str(
            int(d1) + 1) + "/" + str(d2) + "/" + str(d3) + " at " + str(appointment_time) + " P.M. for your checkup.")
        if not results:
            msg.body("Please check your file reference id.")
        responded = True

    # First Time
    if "first time" in incoming_msg or "new patient" in incoming_msg or "i'm new" in incoming_msg and flag == 2:
        flag += 1
        responded = True

    if flag == 3 and len(incoming_msg) > 3:
        msg.body("Please enter your Age")
        flag += 1
        responded = True

    # and len(incoming_msg) > 2
    if flag == 4 and 1 <= len(incoming_msg) <= 3:
        b = str(incoming_msg)
        msg.body("Please enter your Name")
        flag += 1
        responded = True

    # and 2 <= len(incoming_msg) <= 40
    if flag == 5 and len(incoming_msg) >= 5:
        a = str(incoming_msg)
        msg.body("Please enter your Address (#House , Area and City)")
        flag += 1
        responded = True

    #  and len(incoming_msg) == 10
    if flag == 6 and "#" in incoming_msg:
        c = str(incoming_msg)
        msg.body("Please enter your Phone number")
        flag += 1
        responded = True
        red_flag -= 1
        print("Red flag", red_flag)

    if flag == 7 and red_flag == 1:
        d = str(incoming_msg)
        d = randint(6500000000, 9999999999)
        msg.body("Are the above provided details correct? (Yes/no)")
        responded = True

        if incoming_msg == "yes":
            # SQL code to insert patient record into database hospital into table patient
            mycursor = connection.cursor()
            sql = "INSERT INTO patient (name,age,address,file_id,phone) VALUES (%s,%s,%s,%s,%s)"
            args = (a, b, c, file_id, d)
            mycursor.execute(sql, args)
            connection.commit()

            sql2 = "INSERT INTO search (name,doctor,file_id) VALUES (%s,%s,%s)"
            args2 = (a, doctors[doc], file_id)
            mycursor.execute(sql2, args2)
            connection.commit()

            print(mycursor.rowcount, "record inserted")
            flag += 1

    if flag == 8:
        sleep(1)
        msg.body("\nYou've been registered into our records.\n📋 Your file reference id is " + str(
            file_id) + ".\n🩺 Your doctor is: " + str(doctors[doc]) + ".\n📆 Your appointment is on " + str(
            int(d1) + 2) + "/" + str(d2) + "/" + str(d3) + " at " + str(appointment_time) + " P.M.")

    # Internal Medicine
    doctors = ['Dr. Gilbert Nightray', 'Dr. James Dee', 'Dr. Christopher Turk']
    doc = randint(0, 2)

    if incoming_msg == "2" or "internal medicine" in incoming_msg and flag == 1:
        msg.body("Are you here for the first time or for follow-up?")
        flag += 1
        responded = True

    # Follow Up
    if "follow up" in incoming_msg or "i'm old" in incoming_msg and flag == 2:
        msg.body("Please enter your file reference id")
        responded = True
        ref_flag += 1

    if ref_flag == 1 and len(incoming_msg) == 6:
        mycursor = connection.cursor(buffered=True)
        finduser = ("SELECT * FROM search WHERE file_id = %s")
        mycursor.execute(finduser, [(incoming_msg)])
        results = mycursor.fetchall()
        connection.commit()
        if results:
            msg.body("Your appointment for follow up has been confirmed. Please visit our facility on " + str(
                int(d1) + 1) + "/" + str(d2) + "/" + str(d3) + " at " + str(
                appointment_time) + " P.M. for your checkup.")
        if not results:
            msg.body("Please check your file reference id.")
        responded = True

    # First Time
    if "first time" in incoming_msg or "new patient" in incoming_msg or "i'm new" in incoming_msg and flag == 2:
        flag += 1
        responded = True

    if flag == 3 and len(incoming_msg) > 3:
        msg.body("Please enter your Age")
        flag += 1
        responded = True

    # and len(incoming_msg) > 2
    if flag == 4 and 1 <= len(incoming_msg) <= 3:
        b = str(incoming_msg)
        msg.body("Please enter your Name")
        flag += 1
        responded = True

    # and 2 <= len(incoming_msg) <= 40
    if flag == 5 and len(incoming_msg) >= 5:
        a = str(incoming_msg)
        msg.body("Please enter your Address (#House , Area and City)")
        flag += 1
        responded = True

    #  and len(incoming_msg) == 10
    if flag == 6 and "#" in incoming_msg:
        c = str(incoming_msg)
        msg.body("Please enter your Phone number")
        flag += 1
        responded = True
        red_flag -= 1
        print("Red flag", red_flag)

    if flag == 7 and red_flag == 1:
        d = str(incoming_msg)
        d = randint(6500000000, 9999999999)
        msg.body("Are the above provided details correct? (Yes/no)")
        responded = True

        if incoming_msg == "yes":
            # SQL code to insert patient record into database hospital into table patient
            mycursor = connection.cursor()
            sql = "INSERT INTO patient (name,age,address,file_id,phone) VALUES (%s,%s,%s,%s,%s)"
            args = (a, b, c, file_id, d)
            mycursor.execute(sql, args)
            connection.commit()

            sql2 = "INSERT INTO search (name,doctor,file_id) VALUES (%s,%s,%s)"
            args2 = (a, doctors[doc], file_id)
            mycursor.execute(sql2, args2)
            connection.commit()

            print(mycursor.rowcount, "record inserted")
            flag += 1

    if flag == 8:
        sleep(1)
        msg.body("\nYou've been registered into our records.\n📋 Your file reference id is " + str(
            file_id) + ".\n🩺 Your doctor is: " + str(doctors[doc]) + ".\n📆 Your appointment is on " + str(
            int(d1) + 2) + "/" + str(d2) + "/" + str(d3) + " at " + str(appointment_time) + " P.M.")

    if incoming_msg == "hi" or incoming_msg == "hello" and flag == 0:
        # return gesture
        msg.body(
            "Welcome to Sacred Heart Hospital 🏥.\nWhat could I help you with?\nFor example, type\nSee a Doctor 👩🏼‍⚕\nSearch for Symptoms 🔍\nVaccination Status 💉\nOrder Medicines 💊")
        responded = True

        # Reference code in case we want 3rd party auto replies
        """
        if 'quote' in incoming_msg:
            r = request.get('http://api.quotable.io/random')
        if (r.status_code == 200) :
            data = r.json()
            quote = f'{data["content"]}({data["author"]})'
        else:
            quote = "Unable to retrive quote"
        msg.body(quote)
        responded = True
        """

    # Run diagnosis
    global diag_flag
    global symptom_count

    if "diagnosis" in incoming_msg or "symptom" in incoming_msg:
        msg.body("Please type the symptoms you are facing (separated by ',')")
        responded = True
        diag_flag += 1

    if len(incoming_msg) > 3 and "," in incoming_msg and diag_flag == 1:
        tags = incoming_msg.split(",")

        myconnect = connection.cursor(buffered=True)
        findloc = ("SELECT disease, Count(*) FROM symptoms WHERE symptoms LIKE %s LIMIT 1")
        for i in range(0, len(tags)):
            myconnect.execute(findloc, [("%" + tags[i] + "%")])
            result1 = myconnect.fetchall()
            print(result1)  # It shows 'NONE' when a non matching symptom is there...
            symptom_count += 1

        connection.commit()
        print("Symptoms count", symptom_count)
        if (symptom_count) >= 4:
            for i in result1:
                print(i[0])
                loc_print = str(i[0])
                msg.body("You might have " + "*" + loc_print + "*")
                responded = True

        else:
            msg.body("Sorry, I was unable to find a particular disease you may be suffering from.")
            responded = True
    # Diagnosis complete

    # Vaccine Joke
    if "vaccination" in incoming_msg or "vaccine" in incoming_msg:
        msg.body("Sorry, currently Covid-19 vaccines are out of stock. Please visit https://www.cowin.gov.in/home to check more vaccination sites.")
        responded = True

    # Extra features
    # Medicines
    global img_flg
    global im
    if "medicine" in incoming_msg or "medicines" in incoming_msg:
        msg.body("Please send us your File ID to confirm your prescription")
        responded = True
        img_flg += 1

    if img_flg == 1 and len(incoming_msg) == 6:
        mycursor = connection.cursor(buffered=True)
        finduser = ("SELECT * FROM search WHERE file_id = %s")
        mycursor.execute(finduser, [(incoming_msg)])
        results = mycursor.fetchall()
        connection.commit()
        if results:
            msg.body("Your prescription is confirmed. Your medicines will be delivered to your doorstep in 2-3 days 🚚.")
        if not results:
            msg.body("Could not accept you medicine request. Please check your file reference id.")
        responded = True
    # Medicines end

    if not responded:
        msg.body(
            "Sorry, I did not catch that. Must have been a typo or something.\nPlease reply 'Hi' or 'Hello' to access my features...")

    return str(resp)

if __name__ == "__main__":
    symptom_count = 0  # For the tag search
    flag = 0  # For locking if's
    img_flg = 0  # For prescription image
    diag_flag = 0  # For patient diagnosis locking if's
    ref_flag = 0  # For Follow Up if
    a = ""
    b = ""
    c = ""
    d = ""
    im = Image.open("rickroll.png")
    app.run()
