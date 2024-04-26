import socket


def get_response():
    rep, rep_from = sock.recvfrom(1024)
    # print(rep, rep_from)
    try:
        response = rep.decode("utf-8")
    except:
        response = f"Erreur lors du décodage: {rep}"

    return response

def send_command(command, value = None):
    match(command):
        case "battery?":
            sock.sendto("battery?".encode(encoding="utf-8"), tello_address)
            print(get_response())
        case "takeoff":
            sock.sendto("takeoff".encode(encoding="utf-8"), tello_address)
            print(get_response())
        case "streamon":
            sock.sendto("streamon".encode(encoding="utf-8"), tello_address)
            print(get_response())
        case "cw":
            if value:
                sock.sendto(f"cw {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "forward":
            if value:
                sock.sendto(f"forward {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "back":
            if value:
                sock.sendto(f"back {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "right":
            if value:
                sock.sendto(f"right {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "left":
            if value:
                sock.sendto(f"left {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "up":
            if value:
                sock.sendto(f"up {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "down":
            if value:
                sock.sendto(f"down {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "flip":
            if value:
                sock.sendto(f"flip {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "speed":
            if value:
                sock.sendto(f"speed {value}".encode(encoding="utf-8"), tello_address)
                print(get_response())
            else:
                print("Veuillez indiquer une valeur afin de pouvoir exécuter cette commande")
        case "land":
            sock.sendto("land".encode(encoding="utf-8"), tello_address)
            print(get_response())
        case "quit":
            sock.close()
            exit(0)

tello_address = ('192.168.10.1', 8889)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Envoie commande: command")
sock.sendto("command".encode(encoding="utf-8"), tello_address)
get_response()

print("\n---------------------------------------")
print("Voici la liste des commandes possibles:")
print("    - battery? (Récupérer la batterie du drône)")
print("    - streamon (Active la caméra)")
print("    - takeoff (Décollage)")
print("    - cw int (Rotation du drône, int: nombre entre 0 et 360)")
print("    - forward int (Faire avancer le drône, int: 1 = 1cm)")
print("    - back int (Faire reculer le drône, int: 1 = 1cm)")
print("    - left int (Faire aller à gauche le drône, int: 1 = 1cm)")
print("    - right int (Faire aller à droit le drône, int: 1 = 1cm)")
print("    - up int (Faire aller en haut le drône, int: 1 = 1cm)")
print("    - down int (Faire aller en bas le drône, int: 1 = 1cm)")
print("    - flip letter (Faire aller en bas le drône, letter: f, b, r, l)")
print("    - speed int (Modifier la vitesse du drône, int: 1 = 1cm/s)")
print("    - land (Atterrissage)")
print("    - quit (Quitter le programme en fermant la connexion avec le drône)")
print("---------------------------------------\n")

while True:
    userInput = input("Veuillez indiquer une instruction à réaliser: ")

    # On vérifie s'il y a un espace présent, si oui on split dessus afin de séparer la commande du nombre
    if " " in userInput:
        command = userInput.split(" ")[0]
        value = userInput.split(" ")[1]
        try:
            send_command(command, value)
        except Exception as err:
            print(err)
            sock.close()
    else:
        command = userInput
        try:
            send_command(command)
        except Exception as err:
            print(err)
            sock.close()