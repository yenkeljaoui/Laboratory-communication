
import socket

print("open server")
UDP_IP = '0.0.0.0'
UDP_PORT = 9999
dict={}
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
sock.bind((UDP_IP, UDP_PORT))
while True:
  data, addr = sock.recvfrom(1024)
  if addr not in dict.values():
    dict[data.decode()] = addr
  else:
    address_sender=addr
    message=data.decode().split()
    name_addressed=message[0]
    message= ' '.join(message[1:])
    if name_addressed in dict:
       sock.sendto(message.encode(), dict[name_addressed])
       print(f'The addressed: "{dict[name_addressed]}", The message: "{message}"')
    else:
        sock.sendto("The user not exist".encode(),address_sender)