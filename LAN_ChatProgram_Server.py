import socket
import _thread

port = 1111
host = ''
server_name = 'WALL-E'

clients = {}
all_messges = []

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creats a TCP socket
print("[-] Socket Created")

s.bind((host,port))#binds the server ip to a given port
print("[-] Socket Bound to port " + str(port))

s.listen(5)#listens for incoming connections
print("[-] Waiting for a connection....")


#----------------------------------------------------------------


def handle_clients(conn):
	'''handles evrey client after connecting and manages
	recving and sending messages'''
	uname = conn.recv(1024).decode()#saves the first input separately to get the user name of the client
	print('[-] '+uname+' Connected from '+addr[0])
	if uname in clients.keys():#checks if the user name is already in use
		conn.send(('User Name taken, try another one.').encode())
		handle_clients(conn)#calles the function again to redo thr proccess
	
	else:
		clients[uname] = conn #adds the user name and the socket information for it in a dictionary of all the users

		for sock in clients.values():#goes through evrey connected socket and sends it the message
			sock.send(('[-] '+uname+' Connected from '+addr[0]).encode())
		n=0
		while len(all_messges)>n:
			old_message = all_messges[n]
			conn.send((old_message).encode())
			n+=1

		
		while True:# the keeps on going for ever until the loop is broken
			data=conn.recv(1024).decode()#receves message from client
			incoming = (uname+' >> '+data)#adding the user name to the massage
			print(incoming)
			all_messges.append(incoming)#add it to a list to send it newly connected clients
			b = data.split('*')#splits massages if they have an '*' to check if a message has a user name attached to start a private session

			if data == '*exit*':#checks if a massage has '*exit*' in it 
				print (("[-] {} has disconnected.").format(uname))
				conn.send(("[-] You have disconnected").encode())#lets the client know that they have secsessfully disconnected
				conn.close()#closes the client socket
				del clients[uname]#delets the client from the dictionary
				for sock in clients.values():
					sock.send((("[-] {} has left the chat.").format(uname)).encode())#lets the the rest of the clients who left the chat
				break#break the infint loop

			elif data == '*help*':
				"""if the massage is '*help*' it send the cleint the commands of the program"""
				conn.send(('[-] To see the list of connections type *list* \n[-] To talke to just one person type *"The user name of the person" \n[-] When exitting Private chat type "*quite*" \n[-]To close the program type "*exit*", or close the window').encode())

			elif data == '*list*':
				Number_connections = 1
				for i in clients:#goes through the user names
					clients[uname].send((('[{}] '+i).format(Number_connections)).encode())#sends the user name after assidning it a nimber to the client that requsted a list of connections
					Number_connections+=1#counts the number of user names 
			
			elif b[-1] in clients.keys():#checks if the what is attached to the massage after a "*" is a valid user name
				client_chosen=b[-1]
				inseal_msg = ('[-] Private session started')
				clients[uname].send((inseal_msg).encode())#lets the client know he/she is in a private session
				
				while data!='*quit*':#while the clients message is not "*quit*" it keeps sending to only the chosen user
					for i in clients.keys():# goes through user names
						if i==client_chosen:#if the user name inputed matches an existing one
						
							clients[uname].send(('[Private]'+uname+' >> '+data).encode())#the message is sent back to the orginal client 
							clients[i].send(('[Private]'+uname+' >> '+data).encode())# and also sent to the requsted user

					data=conn.recv(1024).decode()#recve messages normaly
					print (uname+' >> '+data)

			else :# if no condition is attached to the message 
				for sock in clients.values():
					sock.send((uname+' >> '+data).encode())#it gets sent to all clients
			
			

#----------------------------------------------------------------
		
while 1:#an infint loop for accepting new connections
	conn,addr=s.accept() #accepts connections
	t = _thread.start_new_thread(handle_clients,(conn,))#opens a new thread for each new client, and acts of the function handle_clients
s.close()#closes the socket when the loop is brocken