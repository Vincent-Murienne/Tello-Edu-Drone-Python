import cv2
import mediapipe as mp
import socket
import time


# Fonction de détection des gestes
def detect_gestures(prev_landmarks, curr_landmarks):
    if prev_landmarks and curr_landmarks:
        # Extraction des coordonnées y du pouce et de l'index pour la main droite
        curr_thumb_y = curr_landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP.value]["y"]
        curr_index_y = curr_landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP.value]["y"]
        
        # Extraction des coordonnées x du pouce et de l'index pour la main droite
        curr_thumb_x = curr_landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP.value]["x"]
        curr_index_x = curr_landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP.value]["x"]
        
        # Extraction des coordonnées x du poignet pour la main droite
        curr_wrist_x = curr_landmarks[mp.solutions.hands.HandLandmark.WRIST.value]["x"]
        
        # Détection du geste "Thumbs Up"
        if curr_thumb_y < curr_index_y and curr_thumb_x < curr_index_x and curr_thumb_x < curr_wrist_x:
            return "Thumbs Up"
        
        # Détection du geste "Thumbs Down"
        if curr_thumb_y > curr_index_y and curr_thumb_x < curr_index_x and curr_thumb_x < curr_wrist_x:
            return "Thumbs Down"
        
        # Détection du geste "OK"
        if abs(curr_thumb_x - curr_index_x) < 0.05 and curr_thumb_y < curr_index_y:
            return "STOP"
        
        # Détection du geste "Doigt d'honneur"
        if curr_thumb_y > curr_index_y and curr_thumb_x > curr_index_x and curr_thumb_x > curr_wrist_x:
            return "FUCK"
        
    return "No Gesture Detected"

def connect_tello(sock, tello_address):
    print("Envoie commande: command")
    sock.sendto("command".encode(encoding="utf-8"), tello_address)
    rep, rep_from = sock.recvfrom(1024)
    print("command" + rep.decode("utf-8"))

    # print("Envoie commande: streamon")
    # sock.sendto("streamon".encode(encoding="utf-8"), tello_address)
    # rep, rep_from = sock.recvfrom(1024)
    # print("streamon" + rep.decode("utf-8"))

def send_action(sock, tello_address, gesture, fuck_bool):
    match(gesture):
        case "Thumbs Up":
            print("Envoie commande: up")
            sock.sendto("up 20".encode(encoding="utf-8"), tello_address)
            rep, rep_from = sock.recvfrom(1024)
            # return rep
        case "Thumbs Down":
            print("Envoie commande: down")
            sock.sendto("down 20".encode(encoding="utf-8"), tello_address)
            rep, rep_from = sock.recvfrom(1024)
            # return rep
        # case "STOP":
        #     print("Envoie commande: land")
        #     sock.sendto("land".encode(encoding="utf-8"), tello_address)
        #     rep, rep_from = sock.recvfrom(1024)
        #     return rep
        case "FUCK":
            if fuck_bool:
                fuck_bool = False
                print("Envoie commande: takeoff")
                sock.sendto("takeoff".encode(encoding="utf-8"), tello_address)
                rep, rep_from = sock.recvfrom(1024)
                # return rep
            else:
                fuck_bool = True
                print("Envoie commande: land")
                sock.sendto("land".encode(encoding="utf-8"), tello_address)
                rep, rep_from = sock.recvfrom(1024)
                exit(0)
                # return rep
            
    return fuck_bool

# Fonction principale
def main():
    fuck_bool = True
    tello_address = ('192.168.10.1', 8889)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Conexion au drône et activation de la caméra
    try:
        connect_tello(sock, tello_address)
    except Exception as err:
        print(err)
        sock.close()
        return

    # Initialisation du détecteur de mains MediaPipe
    hands_detector = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    # Initialisation de la webcam
    camera_video = cv2.VideoCapture(0)
    # drone_video = cv2.VideoCapture("udp://@0.0.0.0:11111")
    camera_video.set(3, 1280)
    camera_video.set(4, 720)

    prev_landmarks = None  # Landmarks de la frame précédente

    # Boucle principale
    while camera_video.isOpened():
        # Lecture de l'image depuis la webcam
        read, frame = camera_video.read()
        if not read:
            continue

        # Conversion de l'image en RGB (MediaPipe nécessite une image RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Détection des landmarks des mains dans l'image actuelle
        results = hands_detector.process(frame_rgb)

        # Affichage des landmarks des mains
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dessin des landmarks sur l'image
                mp.solutions.drawing_utils.draw_landmarks(
                    image=frame,
                    landmark_list=hand_landmarks,
                    connections=mp.solutions.hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )

                # Extraction des landmarks de la main actuelle
                curr_landmarks = [{"x": landmark.x, "y": landmark.y} for landmark in hand_landmarks.landmark]

                # Détection du geste en comparant les landmarks actuels avec ceux de la frame précédente
                gesture = detect_gestures(prev_landmarks, curr_landmarks)
                print(gesture)  # Affichage du geste détecté
                try:
                    fuck_bool = send_action(sock, tello_address, gesture, fuck_bool)
                except Exception as err:
                    print(err)
                    sock.close()
                    return

                # Stockage des landmarks de la frame actuelle pour la prochaine itération
                prev_landmarks = curr_landmarks

        # Affichage de l'image avec les landmarks et les gestes détectés
        cv2.imshow('Hand Gesture Detection', frame)

        # Interruption de la boucle si la touche 'Esc' est pressée
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    # Libération des ressources
    camera_video.release()
    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
