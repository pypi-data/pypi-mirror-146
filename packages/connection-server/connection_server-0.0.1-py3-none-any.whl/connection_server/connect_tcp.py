import sys
import socket

def createConnectionTCP():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
  except socket.error as e:
    print('The conection failed!')
    print('Error: {}'.format(e))
    sys.exit()

  print('Socket was created successfully')

  target_host = input('Enter the host or ip that will be queried:  ')
  target_port = input('Enter the port that will be consulted:  ')

  try:
    s.connect((target_host, int(target_port)))
    print('Client TCP has successfully connected to host: {} -port {}'.format(target_host, target_port))
    s.shutdown(2)
  except socket.error as e:
    print('Could not connect to host: {} -port {}'.format(target_host, target_port))
    print('Error: {}'.format(e))
    sys.exit()
