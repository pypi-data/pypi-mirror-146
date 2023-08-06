import socket

def createConnectionUDP():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  except socket.error as e:
    print('The conection failed!')
    print('Error: {}'.format(e))

  print('Client socket was created successfully')

  target_host = input('Enter the host or ip that will be queried:  ')
  target_port = input('Enter the port that will be consulted:  ')
  message = input('Enter the message that will send:  ')

  try:
    print('Client:' + message)
    s.sendto(message.encode(), (target_host, target_port))

    data, server = s.recvfrom(4096)
    data = data.decode()
    print('Client:' + data)
  finally:
    print('Client: closing the connection')
    s.close()