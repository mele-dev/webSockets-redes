from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

port = 80

try:
    serverSocket.bind(('', port))
    
    serverSocket.listen(1)
    print(f'Servidor listo para recibir conexiones en el puerto {port}...')
    
except Exception as ex:
    print(f'No se pudo establecer la conexión: {ex}')
    sys.exit()

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Conexión aceptada desde {addr}")

    try:
        message = connectionSocket.recv(1024).decode()
        print(f"Mensaje recibido: {message}")

        filename = message.split()[1]
        filepath = filename[1:] 

        # aca abrimos el archivo 
        with open(filepath, 'r') as f:
            outputdata = f.read()

        # mandamos el encabezado http 200 
        response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response_header.encode())

        # mandamos al cliente...
        connectionSocket.send(outputdata.encode())

    except IOError:
        # manejamos la excepcion por si pasa algo con el archivo
        error_message = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
        connectionSocket.send(error_message.encode())

    except Exception as ex:
        # en esta excepcio entra si pasa algo que no sea relacionado al archivo
        print(f'Error inesperado: {ex}')

    finally:
        # cerramos la conexion con el socket
        connectionSocket.close()