import socket
from time import sleep
import struct


def getcommand(sock):
    commande = bytes()
    while len(commande)<3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def getresult(sock):
    data = bytes()
    while len(data) != 8:
        data += sock.recv(8 - len(data))
    return struct.unpack("d", data)[0]


def understand_set_command(sock):
    n = getresult(sock)
    m = getresult(sock)

    return n, m


def understand_hum_command(sock):
    nb_homes = getresult(sock)

    coordinates = []
    for i in range(nb_homes):
        x = getresult(sock)
        y = getresult(sock)
        coordinates += [(x,y)]

    return coordinates


def understand_hme_command(sock):
    x = getresult(sock)
    y = getresult(sock)

    return x,y


def understand_upd_command(sock):
    nb_changes = getresult(sock)

    coordinates = []
    for i in range(nb_changes):
        x = getresult(sock)
        y = getresult(sock)
        humans = getresult(sock)
        vampires = getresult(sock)
        werewolves = getresult(sock)
        coordinates += [(x,y)]

    return coordinates


def send_nme_command(sock, command, name):
    paquet = bytes()
    paquet += command.encode()
    paquet += struct.pack("d", name.length)
    paquet += name.encode()
    sock.send(paquet)


def send_mov_command(sock, command, movements):
    paquet = bytes()
    paquet += command.encode()
    paquet += struct.pack("d", movements.length)

    for movement in movements:
        paquet += struct.pack("d", movement[0])
        paquet += struct.pack("d", movement[1])
        paquet += struct.pack("d", movement[2])
        paquet += struct.pack("d", movement[3])
        paquet += struct.pack("d", movement[4])

    sock.send(paquet)


if __name__ == '__main__':
    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 555))

    while True:
        cmd = getcommand(sock)

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
        elif cmd == u"END":
            break
        elif cmd == u"BYE":
            sleep(1)
            continue
        else:
            raise ValueError("Erreur protocole")

        sleep(1)