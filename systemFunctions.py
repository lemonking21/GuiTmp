import re
from tkinter import Button, Menu, Toplevel, Label, Text, PanedWindow , VERTICAL, END, messagebox
from tkinter.filedialog import askopenfilename
import smtplib
from email.mime.text import MIMEText                    
from email.mime.multipart import MIMEMultipart          
from email.mime.base import MIMEBase                    
from email import encoders
import os.path          
import datetime
#############################################################
#############################################################
#Created By Kyle Howard Krug
#Created ON 7/11/2019
#This was created to function as a basic gui template for all
#Future programs that may need it
#This is a live code, it can be edited at any point, so make 
#to keep a few backups
#Last updated on 7/11/2019
#############################################################
#############################################################
#Global Varibles
filename =''
#############################################################
def file_update(about):
    name = select_file()
    about.delete('1.0', END)
    about.insert('1.0',name)
    about.config(state= 'disable')
#############################################################
# Template for a the main window
#############################################################
def main_win(i):
    i.title('Main Window')
    i.geometry('1000x500')
    p = PanedWindow(i, orient= VERTICAL, height = 10, width = 30, bg = 'green')
    p.pack(side = 'bottom')
    about=Text(p, height = 1, width = 50)
    about.pack()
    fbtn= Button(p, text = "Upload A File", command = lambda: file_update(about))
    fbtn.pack(side= 'bottom')
    win_menu(i)
    close_btn(i)
#############################################################
# Template for a new pop up window
#############################################################
def open_wind(i):
    i_win = Toplevel(i)
    i_win.attributes('-topmost',1)
    return i_win
#############################################################
#############################################################
# Template for the menu bar
#############################################################
def win_menu(i):
    menu= Menu(i)
    i.config(menu=menu)
    file= Menu(menu)
    view = Menu(menu)
    email = Menu(menu)
    about = Menu(menu)

    file.add_command(label = 'exit', command = i.destroy)
    menu.add_cascade(label = 'File', menu = file)

    view.add_command(label = 'Full Screen',  command= lambda:i.geometry("{0}x{1}+0+0".format(i.winfo_screenwidth(), i.winfo_screenheight())))
    view.add_command(label = 'Original Size',  command= lambda:i.geometry('1000x500'))
    view.add_command(label = 'Small',  command= lambda:i.geometry('200x200'))
    menu.add_cascade(label = 'View', menu = view)

    email.add_command(label ='Send To', command = lambda:email_win(i) )
    menu.add_cascade(label = 'Email Options', menu = email)

    about.add_command(label = 'Info',command = lambda:about_win(i))
    menu.add_cascade(label = 'About', menu = about)
#############################################################
#############################################################
# The pop up about window on the menu bar
#############################################################
def about_win(i):
    a= open_wind(i)
    a.title("About")
    a.geometry('400x400')
    about  = Text(a, height = 300, width = 300)
    about.insert('1.0','Created by: Kyle Howard Krug\nCreated on:7/11/2019\nCreated to provide a basic gui setup\nVersion Number: 0.0.1')
    about.config(state= 'disable')
    about.pack()
    close_btn(a)
#############################################################
#############################################################
# The pop up email window on the menu bar
#############################################################
def email_win(i):
    e=open_wind(i)
    e.title('Email Window')
    e.geometry('200x120')
    p = PanedWindow(e, orient= VERTICAL, height = 50, width = 30)
    p.pack()
    close_btn(e)
    emailText= Label(p, text = 'Please enter the email\nto send the selecte file to')
    emailText.pack(side='top')
    text = Text(p,height = 1, width = 30, bg = 'white', bd=  2)
    text.pack(side= 'bottom')
    subBTN= Button(p,text = 'Submit',command = lambda:checkEmail(text,e))
    subBTN.pack()
#############################################################
#############################################################
# Close button
#############################################################
def close_btn(i):
    btn= Button(i, text = 'close', command = i.destroy)
    btn.pack(side = 'right', expand = 1)
#############################################################
#############################################################
# File selection option
#############################################################
def select_file():
    name = askopenfilename(initialdir="C:/Users/",
                           filetypes =(("CSV File", "*.csv"),("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file.")
    set_file_name(name)
    #try:
        #with open(name,'r',newline = '') as UseFile:
            #print(UseFile.read())
   # except:
        #print("No file exists")
    set_file_name(name)
    return name
#############################################################
#############################################################
# Set file name
#############################################################
def set_file_name(name):
    global filename
    filename = name
#############################################################
#############################################################
# get the file name function
#############################################################
def getFilename():
    global filename
    return filename
#############################################################
#############################################################
# Function to check if the email is in the current format
#############################################################
def checkEmail(text,i):
    email = text.get('1.0',END)
    format_email='^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-z]{2,4})$'
    match = re.match(format_email, str(email))
    if match == None:
        text.delete('1.0', END)
        push_sub(text,i)
    else:
        send_email(email,getFilename())
        i.destroy()
#############################################################
#############################################################
# Error message for if the code is in incorrect format
#############################################################
def push_sub(text, i): 
    messagebox.showinfo('Error' , 'Incorrect email format, please reenter the \n address you want to send the file to.')
############################################################## 
#############################################################
# Setting up and sending an email
#############################################################
def send_email(rEmail,getFile):
    myemail = 'TestAutomated12@gmail.com'
    mypassword = '1234567_AB'# your email password
    #rEmail = ''# recipents email, to add more simple use a list
    subject= '[Auto Generated] ... Report'
    #msg = open('AutoMessage.txt')
    with open('AutoMessage.txt', 'r') as file:
        msg = file.read()
    msg = msg + '\nTime completed: ' + str(datetime.datetime.now())
    file_loc= getFile# location of the file
    #setup for the attachment on the
    file_name = os.path.basename(file_loc)
    print(file_name)
    attach = open(file_loc, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attach.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

    message = MIMEMultipart()
    message['From'] = myemail
    message['To'] = rEmail
    message['Subject']= subject
    message.attach(MIMEText(msg, 'plain'))
    message.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587) # if 587 doesn't work try 25 or 465 / office365
    server.starttls()
    server.login(myemail, mypassword)
    text= message.as_string()
    server.sendmail(myemail, rEmail, text)
    server.quit()
    #############################################################
#############################################################
#############################################################
#############################################################
#############################################################