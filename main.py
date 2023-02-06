import cv2

import drone
from scene import SoftwareRender

target_path = 'main_folder/'
N = 2
Frame = 3


def get_drones_from_file(filename, drone_name, translations, rotations, videoCaps):
    coordinates = (100, 100)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (255, 0, 255)
    thickness = 2
    image_num = 0
    with open(filename + drone_name + '/status.txt') as f:
        for line in f:
            if line.startswith('img num:'):
                image_num = [int(i) for i in line.split() if i.isdigit()]
            elif line.startswith('['):
                line = line.replace('[', '')
                translations.append([float(i) for i in line.split(", ")[0:3]])
                # rotations_ = line.split()[1:]
                # rotations.append([int(rotation_.split('/')[0]) for rotation_ in rotations_])
    for i in range(Frame):
        img = cv2.imread(filename + drone_name + '/video_cap/' + str(i + 1) + '.jpg')
        img = cv2.putText(img, drone_name + ' ,Frame ' + str(i+1), coordinates, font, fontScale, color, thickness,
                          cv2.LINE_AA)
        videoCaps.append(img)


if __name__ == '__main__':

    drones = []
    for i in range(N):
        drone_name = 'drone_name' + str(i + 1)
        translations, rotations, videoCaps = [], [], []
        get_drones_from_file(target_path, drone_name, translations,
                             rotations, videoCaps)
        droneX = drone.Drone()
        droneX.name = 'drone' + str(i + 1)
        droneX.position = translations
        droneX.rotation = rotations
        droneX.videoCaps = videoCaps
        drones.append(droneX)

    app = SoftwareRender(drones)
    app.run()
    cv2.destroyAllWindows()
