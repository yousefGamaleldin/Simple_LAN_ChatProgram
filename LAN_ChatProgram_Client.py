import socket
import _thread
from tkinter import*

#---------------------The main functions-------------------------------------------

def sending(event=None):# this fuction gets triggred by an event or action
	messages = Tmessages.get()#gets the message from the Entry in the UI
	Tmessages.set('')#clears the feald after sending the message
	s.send(messages.encode())#sends the message to the server

def recving():
	while True:#while the loop is intact the client keeps receving data from the server 
		data = s.recv(1024).decode()#recve data from server 
		message_listbox.insert(END,data)#display it on the listbox
		
		if len(data) == 0:#if the data from the server stops, it means the connection is closed
			s.close()#close the client socket 
			root.destroy()#closes the UI window
			break #break the recving loop


def exitting(event=None):# this fuction gets triggred by an event or action
	Tmessages.set('*exit*')#makes the message equal '*exit*'
	sending()#and trigger the sending function to send it as a message
#----------------------The chat interface------------------------------------------

root = Tk() #the chat room window
root.title('Welcome')

message_frame = Frame(root)#a fream to hold elments
message_frame.grid(row=0,columnspan=2)

Tmessages = StringVar()#a string input liked to the UI

scrollbar = Scrollbar(message_frame)
scrollbar.pack(side=RIGHT,fill=Y)

message_listbox = Listbox(message_frame,width=40,height=20,yscrollcommand=scrollbar.set)
message_listbox.pack(side=LEFT,fill=BOTH)# list to display all the messages in


message_entry = Entry(root,width=35,textvariable=Tmessages)
message_entry.bind('<Return>',sending)#binding an entry to function by a keyboard key
message_entry.grid(row=2, column=0)

send_button = Button(root,text='Send',command=sending)
send_button.grid(row=2,column=1)

root.protocol("WM_DELETE_WINDOW",exitting)#this protocol means when the window is closed abruptly, and triggres a function

#-----------------------Starting the socket-------------------------------------

def info(event):# this fuction gets triggred by an event
	host = E_IP.get()
	port = 1111
	uname = E_user_name.get()
	s.connect((host,port))#looks for a server in the given Port and Ip and connectes to it
	s.send(uname.encode())#send the user name to the server to identfy the client
	_thread.start_new_thread(recving,())#start a separate thread to recve messages
	sign_up.destroy()#closes the signup window 
	root.mainloop()#keeps running the chat window

#----------------------The sign up interface------------------------------------------

sign_up = Tk()# a window to sign up from
sign_up.title('Sign Up')

L_IP = Label(sign_up,text='Server IP ')# label for the IP
L_user_name = Label(sign_up,text='User Name ')#label for the user name

IP = StringVar()
username = StringVar()

E_IP = Entry(sign_up,text='Server IP ',textvariable=IP)#an intry for the IP
E_user_name = Entry(sign_up,text='User Name ',textvariable=username)#entry for the user name

'''select where evry elment is shown in the window'''
L_IP.grid(row=1,column=1)
L_user_name.grid(row=3,column=1)
E_IP.grid(row=1,column=2)
E_user_name.grid(row=3,column=2)

'''trigring the function info() when the Enter key is pressed'''
E_IP.bind('<Return>',sign_up)
E_user_name.bind('<Return>',sign_up)


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creats a TCP socket
sign_up.mainloop()#keeps on running the window


