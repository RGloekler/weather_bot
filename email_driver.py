#!/usr/bin/python3
from cryptography.fernet import Fernet
from email.message import EmailMessage
import smtplib, os.path, sys

from getpass import getpass

# checks for existing user data and encrypts login credentials for program use
def encrypt_email():
    # if the data file is not in the PATH...
    if not os.path.isfile('email_data.txt'):
        key = Fernet.generate_key()
        f = Fernet(key)
        # open a file in write mode for byte data
        file = open('email_data.txt', 'wb')
        file.write(f.encrypt(input('Enter your gmail username: ').encode()))
        file.write('\n'.encode())
        file.write(f.encrypt(input('Enter your gmail password (to be encrypted): ').encode()))
        file.write('\n'.encode())
        file.write(key)
        file.close()

        file = open('email_data.txt', 'rb')
        login = file.readlines()
        file.close()
    else:
        # otherwise the data has previously been encypted,
        # so we should decrypt the value for program use
        file = open('email_data.txt', 'rb')
        login = file.readlines()
        file.close()
    return login

# sends email containing relevent information
def send_email(msg, usrname, password):
    fromaddr = usrname
    toaddrs  = usrname
    username = usrname

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(usrname, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# need to add in functionality for hyperlinks to store pages...
def main():
    usr_data = encrypt_email()
    f = Fernet(usr_data[2])

    # make sure the element reference is not stale and we can access data
    stale = True
    SUBJECT = 'Updated Stock Info'
    message = 'Subject: {}\n\n{}'.format(SUBJECT, 'Here is the updated weather report:\n' + 'kljasdfjkldsfaklj;sadf;ljk')

    if (stale): #'In Stock' in TEXT):
        print('Sending email...')
        try:
            send_email(message, f.decrypt(usr_data[0]).decode('utf-8'), f.decrypt(usr_data[1]).decode('utf-8'))
        except Exception as exception:
            print(type(exception))
            print('Could not send email, please check login.')
    else:
        print('No new stock, terminating.')


if __name__ == "__main__":
    main()
    sys.exit()
