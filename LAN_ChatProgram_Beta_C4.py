import socket
import _thread

def sending():
	while True:
		massege = input()
		s.send(massege.encode())




def recving():
	while True:
		data = s.recv(1024).decode()
		a = data.split(',')
		p_port = a[-1]

		if '**star_server' in data:
			private_server()
		
		elif '**start client' in data:
			private_client()
		
		elif '*quite*' in data:
			s.close()
		
		else:
			print(data)





def private_server():

	s_port=int(input('[*] Enter port: '))
	s_host=''
	server_name = 'WALL-E'


	s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("[-] Socket Created")

	s2.bind((s_host,s_port))
	print("[-] Socket Bound to port " + str(s_port))

	s2.listen(5)
	print("[-] Waiting for a connection....")

	def handle_clients(conn):
		uname = conn.recv(1024).decode()
		print('[-] '+uname+' Connected.')
		clients[uname] = conn

		while True:
			data=conn.recv(1024).decode()
			print (uname+' >> '+data)
			b = data.split('*') 
			if b[-1] in clients.keys():
				x=b[-1]
				for i in clients.keys():
					if i == x:
						clients[uname].send((' >> '+data).encode())
						clients[i].send((' >> '+data).encode())

					elif data!='*quite*':
						for sock in clients.values():
							sock.send((uname+' >> '+data).encode())
					else:
						pass

	while 1:
		conn,addr=s.accept()
		print('[-]',addr[0],"has connected.")
	s.close()






def private_client():
	
	def sending2():
		while True:
			massege = input()
			s2.send(massege.encode())

	def recving2():
		while True:
			data = s2.recv(1024).decode()
			print(data)

			if '*quite*' in data:
				s2.close()

	
	p_host = input('[*] Enter Host IP: ')
	p_port = int(input('[*] Enter Port: '))
	p_uname = 'Hope'

	s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s2.connect((p_host,p_port))
	s2.send(p_uname.encode())

	_thread.start_new_thread(sending2,())
	_thread.start_new_thread(recving2,())

	sending2()
	recving2()




host = input('[*] Enter Host IP: ')
port = int(input('[*] Enter Port: '))
uname = input('[*] Enter User Name: ')
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
s.send(uname.encode())
_thread.start_new_thread(sending,())
_thread.start_new_thread(recving,())

sending()
recving()