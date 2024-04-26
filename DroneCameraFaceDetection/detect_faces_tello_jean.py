import cv2
from djitellopy import tello
from mesh_face_detector import FaceMeshDetector
import time


def pixels_to_cm(pixels):
    # dist IRL 155cm = 85 pixels de large
    return (85*155)/pixels

def pixels_to_cm_strafe(pixels):
    # dist IRL 155cm: 236 pixels de large = 30cm
    return (236*30)/pixels

def get_face_distance(frame, faces):
    if faces is not None and len(faces) > 0:
        x_min, x_max, y_min, y_max = faces[0]
        pixels = x_max - x_min
        dist = pixels_to_cm(pixels)
        cv2.putText(frame, f"Distance: {dist}", (10, 75), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 1)
        return dist

def move_x(frame, faces):
    dist = get_face_distance(frame, faces)
    if dist is not None and int(dist) != 110:
        x = 110-int(dist)
        if x >= 20:
            return int(-x)
        elif x <= -20:
            return int(abs(x))

def move_y(frame, faces):
    dist = get_face_distance(frame, faces)
    if dist >= 100 and dist <= 120:
        width, height = frame.shape[:2]
        center = width/2
        center_face = ((faces[0][0]-faces[0][1])/2)+faces[0][0]
        # if center_face < center-20:
        #     dist_pixels = center - center_face
        #     dist_cm = pixels_to_cm_strafe(dist_pixels)
        #     print(center, center_face, dist_pixels, dist_cm)
        #     return int(dist_cm)
        # elif center_face > center+20:
        #     dist_pixels = center - center_face
        #     dist_cm = pixels_to_cm_strafe(dist_pixels)
        #     print(center, center_face, dist_pixels, dist_cm)
        #     return int(dist_cm)
        if center_face < center-40:
            return 20
        elif center_face > center+20:
            return -20

def follow_face(drone, frame, faces):
    if faces is not None:
        # Gère la distance (avancer / reculer)
        x = move_x(frame, faces)

        # Gère le strafe (droite / gauche)
        y = move_y(frame, faces)
        # y=0

        z = 0

        if x is None:
            x = 0
        
        if y is None:
            y = 0
        
        if z is None:
            z = 0

        if x != 0 or y != 0 or z != 0:
            print(x,y)
            drone.go_xyz_speed(x, y, z, 10)
            print(x,y)

def run_tello_video(drone, detector):
    while True:
        frame = drone.get_frame_read().frame
        faces = detector.detect_faces(frame)
        follow_face(drone, frame, faces)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break
    cv2.destroyAllWindows()


def main():
    effect = 'blur'
    mesh_detector = FaceMeshDetector(effects=effect)
    
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    drone.query_battery()
    drone.takeoff()
    time.sleep(3)
    drone.move_up(100)
    run_tello_video(drone, detector=mesh_detector)


if __name__ == "__main__":
    main()
