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
        passwd = getpass()
        file.write(f.encrypt(passwd.encode()))
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
    if len(sys.argv) != 2:
        print("usage: \'python3 email_driver.py <data file>\"" )
        exit()
        
    filenm = sys.argv[1]
    print(filenm)
    usr_data = encrypt_email()
    f = Fernet(usr_data[2])

    data_file = open(filenm, 'r')
    TEXT = '' # empty string for contents of the email
    TEXT = data_file.read()
    
    # make sure the element reference is not stale and we can access data
    stale = True
    SUBJECT = 'Updated Weather Info'
    
    message = 'Subject: {}\n\n{}'.format(SUBJECT, 'Here is the updated weather report:\n' + TEXT)

    if (stale): #'In Stock' in TEXT):
        print('Sending email...')
        try:
            send_email(message, f.decrypt(usr_data[0]).decode('utf-8'), f.decrypt(usr_data[1]).decode('utf-8'))
        except Exception as exception:
            print(type(exception))
            print('Could not send email, please check login.')
        exit()


if __name__ == "__main__":
    main()
    sys.exit()
