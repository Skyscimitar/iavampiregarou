import socket
from time import sleep
import struct


def getcommand(sock):
    commande = bytes()
    while len(commande)<3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def getint(sock):
    data = bytes()
    data += sock.recv(1)
    #print(data)
    return int.from_bytes(data, byteorder='big')


def understand_set_command(sock):
    n = getint(sock)
    m = getint(sock)
    return n, m


def understand_hum_command(sock):
    nb_homes = getint(sock)

    coordinates = []
    for i in range(nb_homes):
        x = getint(sock)
        y = getint(sock)
        coordinates += [(x,y)]

    return coordinates


def understand_hme_command(sock):
    x = getint(sock)
    y = getint(sock)

    return x,y


def understand_upd_command(sock):
    nb_changes = getint(sock)

    coordinates = []
    for i in range(nb_changes):
        x = getint(sock)
        y = getint(sock)
        humans = getint(sock)
        vampires = getint(sock)
        werewolves = getint(sock)
        coordinates += [(x,y,humans,vampires,werewolves)]

    return coordinates


def send_nme_command(sock, name):
    paquet = bytes()
    paquet += 'NME'.encode()
    paquet += struct.pack("d", len(name))
    paquet += name.encode()
    sock.send(paquet)


def send_mov_command(sock, movements):
    paquet = bytes()
    paquet += 'MOV'.encode()
    paquet += bytes([len(movements)])
    print(movements)

    for movement in movements:
        print(movement)
        print(movement[0])
        paquet += bytes([movement[0]])
        paquet += bytes([movement[1]])
        paquet += bytes([movement[2]])
        paquet += bytes([movement[3]])
        paquet += bytes([movement[4]])
        print(paquet)
        #paquet += struct.pack("d", movement[0])
        #paquet += struct.pack("d", movement[1])
        #paquet += struct.pack("d", movement[2])
        #paquet += struct.pack("d", movement[3])
        #paquet += struct.pack("d", movement[4])

    sock.send(paquet)


if __name__ == '__main__':
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 5555))
    print('Connecté')
    send_nme_command(sock, 'helene')

    while True:

        while True :
            cmd = getcommand(sock)
            #print('commande reçue :' + cmd )
            if cmd == u"SET":
                print ("SET command:", understand_set_command(sock))
            elif cmd == u"HUM":
                print("HUM command:", understand_hum_command(sock))
            elif cmd == u"HME":
                print("HME command:", understand_hme_command(sock))
            elif cmd == u"MAP":
                print("MAP command:", understand_upd_command(sock))
            elif cmd == u"UPD":
                print("UPD command:", understand_upd_command(sock))
                break
            elif cmd == u"END":
                break
            elif cmd == u"BYE":
                sleep(1)
                continue
            else:
                raise ValueError("Erreur protocole")

        send_mov_command(sock,[(4,3,4,4,4)])

        sleep(1)