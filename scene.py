import cv2
import pygame

import button
from object_3d import *
from camera import *
from projection import *
from button import *
import pygame as pg


delay = 10000
Auto = True
num_frame = 3
N = 2


class SoftwareRender:
    def __init__(self, drones):
        self.drones = drones
        self.frame = 1
        self.world_axes = Axes
        self.obj = None
        self.objects = []
        self.projection = None
        self.camera = None
        self.IMGFlag = False
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 500, 500
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [20, 20, -80])
        self.projection = Projection(self)
        self.world_axes = Axes(self)
        self.world_axes.scale(30)

        i = 0
        for drone in self.drones:
            self.obj = self.get_object_from_file('cube.obj')
            self.obj.name = drone.name
            self.obj.draw_name = True
            self.obj.draw_normals = False
            self.obj.normal = drone.position[self.frame]
            self.obj.translate(drone.position[self.frame - 1])
            self.objects.append(self.obj)
            i += 1
        # object1.rotate_y(-math.pi / 8)

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        self.world_axes.draw()
        for obj in self.objects:
            obj.draw()

    def replace_drones(self):
        # self.objects.clear()
        i = 0
        if self.frame <= num_frame:
            for drone in self.drones:
                self.obj = self.get_object_from_file('cube.obj')
                self.obj.name = drone.name
                self.obj.draw_name = True
                self.obj.draw_normals = False
                self.obj.translate(drone.position[self.frame - 1])
                self.objects.append(self.obj)
                i += 1

    def slice_pics(self):
        imgs = []
        img = None
        cv2.namedWindow("imgs", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("imgs", self.WIDTH, self.HEIGHT)
        if not self.IMGFlag:
            for drone in self.drones:
                imgs.append(drone.videoCaps[self.frame - 1])
            if N == 1:
                img = imgs[0]
            elif N == 2:
                img = np.concatenate((imgs[0], imgs[1]), axis=0)
            elif N == 3:
                img = np.concatenate((imgs[0], imgs[1], imgs[2]), axis=0)
            elif N == 4:
                img = np.concatenate(((np.concatenate((imgs[0], imgs[1]), axis=1)),
                                     (np.concatenate((imgs[2], imgs[3]), axis=1))), axis=0)
            self.IMGFlag = True
        if imgs:
            cv2.imshow('imgs', img)

    def run(self):
        ######################################################################################
        start_img = pygame.image.load(r'images\back.png').convert_alpha()
        backButton= button.Button(0, 0, start_img, 50)
        if backButton.draw(self.screen):
            print('BACK')
        ######################################################################################
        if Auto:
            while True:
                self.draw()
                self.camera.control()
                [exit() for i in pg.event.get() if i.type == pg.QUIT]
                pg.display.set_caption('frame :' + str(self.frame) + ' ,time : ' + str(pg.time.get_ticks()))
                pg.display.flip()
                self.clock.tick(self.FPS)
                self.slice_pics()

                if pg.time.get_ticks() > delay * self.frame:
                    self.frame += 1
                    self.replace_drones()
                    self.IMGFlag = False
                if self.frame > num_frame:
                    break
        else:
            while True:
                self.draw()
                self.camera.control()

                [exit() for i in pg.event.get() if i.type == pg.QUIT]
                pg.display.set_caption('frame :' + str(self.frame) + ' ,time : ' + str(pg.time.get_ticks()))
                pg.display.flip()
                self.clock.tick(self.FPS)
                # slice_pics(self.frame)
                img1 = cv2.imread('lena.jpg')
                cv2.imshow('VideoCap', img1)

                if pg.time.get_ticks() > delay * self.frame:
                    self.frame += 1
                    if self.frame > 3:
                        break
