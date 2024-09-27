from socket import *
import sys # Para finalizar el programa

serverSocket = socket(AF_INET, SOCK_STREAM)
port = 80

try:
    serverSocket.bind(('', port))
    # el 1 es el tamaño máximo de la cola de conexiones. Solo puede haber una conexion a la vez.
    serverSocket.listen(1)
except Exception as ex:
    print(f'No se pudo estabecer la conexion {ex}')

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Conexión aceptada desde {addr}")

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()

    except IOError:
        print(f'Archivo no encontrado!')
        serverSocket.close()
        sys.exit()