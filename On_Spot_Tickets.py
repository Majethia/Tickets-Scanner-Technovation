import pyqrcode
import sqlite3
import hashlib
import requests

connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()

HTML = '''
<div style='text-align:center;'><img
        src='https://lh3.googleusercontent.com/WpmmMXhvSnF1lEKVzetbqq92rAcSX_eHVNnzuV8d-W3LOw89cTHsUZJHX1e-o6fNVlTfelSAyVpB_oS5fFVJH4j9jqFoHXLwAYTu12ZF'
        style='display:block; margin:auto;' /></div><br><br>
<div style='text-align:center;'>
    <div style='display:inline-block;text-align:left;'>
        <p style='display:block; margin:auto; color: black; font-weight:600;'>
            Greetings, [name]<br>
            <br>
            Thank you for registering for [event]<br>
            This mail contains more information about the event that may come
            handy.<br>
            <br>
            The rules & regulations for the event are given below.<br>
            Link: <a href=' https://drive.google.com/file/d/1-DIVeKLtYZBRbOucOf3smN1gOe1HkxNN/view?usp=drivesdk'>https://drive.google.com/file/d/1-DIVeKLtYZBRbOucOf3smN1gOe1HkxNN/view?usp=drivesdk</a><br>
            <br>
            We hope to deliver a memorable experience to you.</p>
    </div>
</div><br><br>
<h3 style='text-align: center;'>Given QR CODE represents your<br>ENTRY TICKET</h3>
<p style='text-align: center;'>Check attachment</p>
'''

def sendAttachMentMail(Id, Name, Email, event):
    html = HTML.replace("[name]", Name).replace("[event]", event)
    url = 'https://mailsender-7ju2.onrender.com/attachmentMail'

    file_path = f'on_spot/{Id}.png'

    with open(file_path, 'rb') as f:
        response = requests.post(url, files={'file': f}, data={'from':'dsaii.dit@gmail.com', 'pass': "zycolfarjjmxesxu", "to" :Email, 'content':"", "subject": f"{event} Ticket", "html": html})

    if response.status_code == 200:
        print('Registration Completed and Email Sent!')
    else:
        print('Error sending email')

def Register(Name, Email, Number, event):
    query = f"INSERT INTO on_spot_tickets(Name, Email, Number) values('{Name}', '{Email}', '{Number}')"
    cur.execute(query)
    connection.commit()
    id = cur.lastrowid
    hash = hashlib.md5(bytes(id))
    qr = pyqrcode.create(f"DSAII-ONSPOT-{event.upper()}-ID-{id}-{hash.hexdigest()[:4]}")
    qr.png(f'on_spot/{id}.png', scale = 8)
    sendAttachMentMail(id, Name, Email, event)

if __name__ == "__main__":
    while True:
        event = input("Event: ").upper()
        Name = input("Name: ")
        Email = input("Email: ")
        Number = input("Number: ")
        
        print(f"\n\nPlease Confirm These Details:\nEvent: {event}\nName: {Name}\nEmail: {Email}\nNumber: {Number}\n\n")
        f = input("Do you want to continue? (y for yes, n for no, e to exit loop)\n")
        if f == "y":
            Register(Name, Email, Number, event)
        elif f == "e":
            break
        else:
            pass