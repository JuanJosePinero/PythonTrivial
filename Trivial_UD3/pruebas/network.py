import socket
import pickle

#handle communication with connected client
#pickle decomposes object data into bytes "0""1"

class Network():
    def __init__(self):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server="192.168.68.111"
        self.port=5555
        self.addr=(self.server, self.port)
        self.p=self.connect()

    def getP(self): #gets info about connection status of ID from server
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")
            return None  # Retorna None si la conexión falla

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()

    if player is None:
        print("Error al conectar con el servidor. Finalizando el juego.")
        return  # Finaliza si no hay conexión

    player = int(player)
    print("You are Player", player)

    def send(self, data): #send and recv response
        try:
            self.client.send(str.encode(data)) #sending data as bytes
            return pickle.loads(self.client.recv(2048)) #recv and de-pickle response frm server
        except socket.error as e:
            print(e)
            
if __name__ == "__main__":
    main()


