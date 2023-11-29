import socket, threading

HOST = input('Введите хост сервера: ')
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
        for client in clients:
            client.send(message)


def handle(client):
        while True:
            try:
                message = client.recv(1024)
                print(f"{nicknames[clients.index(client)]} отправил сообщение {message}")

                broadcast(message)

            except:
                index = clients.index(client)

                clients.remove(client)
                client.close()

                nickname = nicknames[index]
                nicknames.remove(nickname)
                break


def receive():
    while True:
            client, address = server.accept()
            print(f"Клиент присоединился с {str(address)}")

            client.send("Имя".encode('utf-8'))
            nickname = client.recv(1024)

            nicknames.append(nickname)
            clients.append(client)

            print(f"Имя клиента {nickname}")
            broadcast(f"{nickname} присоединился к серверу!\n".encode('utf-8'))
            client.send("Присоединился к серверу".encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()


print(f"Сервер запущен: IP {HOST} PORT {PORT}")
receive()