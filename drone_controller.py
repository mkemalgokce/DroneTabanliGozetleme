from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
from datetime import datetime

# Speed of the drone
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 120


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

        self.mode = 0
        self.modeText = "Normal"
    def run(self):

        self.tello.connect()
        self.tello.set_speed(self.speed)

        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        isFirst = True
        isRotating = False
        saveTime = time.time()
        while not should_stop:
            
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            
            screenFrame = frame.copy()
            if self.mode == 1: 
                self.modeText = "Active"
                if time.time() - saveTime > 0.3:
                    print("Saving !")
                    saveTime = time.time()
                    cv2.imwrite('goruntuler/droneKayit/'+datetime.now().strftime("%Y.%m.%d-%H:%M:%S.%f")[:-4] +".png", frame)
            elif self.mode == 2:
                if isFirst:
                    tic = time.time()
                    isFirst = False
                
                toc = time.time()
                if toc - tic > 6:
                    print("180")
                    self.yaw_velocity = 180
                    self.for_back_velocity = 0
                    isRotating = True
                    rotatingTime = time.time()
                    tic = time.time()
                else: 
                    if isRotating:
                        print("Rotating")
                        if time.time() - rotatingTime > 2:
                            isRotating = False
                            print("Falsed")
                    else:
                        print("Normal")
                        self.yaw_velocity = 0
                        self.for_back_velocity = 10                 
                if time.time() - saveTime > 0.3:
                    print("Savingg !")
                    saveTime = time.time()
                    cv2.imwrite('goruntuler/droneKayit/'+datetime.now().strftime("%Y.%m.%d-%H:%M:%S.%f")[:-4] +".png", frame)
                self.modeText = "Saving"
                
            else:
                self.modeText = "Normal"
            text = "Battery: {}%".format(self.tello.get_battery())
            
            
            cv2.putText(screenFrame, text, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(screenFrame, self.modeText, (5, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            screenFrame = cv2.cvtColor(screenFrame, cv2.COLOR_BGR2RGB)
            screenFrame = np.rot90(screenFrame)
            screenFrame = np.flipud(screenFrame)
            
            screenFrame = pygame.surfarray.make_surface(screenFrame)
            self.screen.blit(screenFrame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False
        elif key == pygame.K_m:
            if self.mode == 1:
                self.mode = 0 
            else:
                self.mode = 1
        elif key == pygame.K_n:
            if self.mode == 2:
                self.mode = 0 
            else:
                self.mode = 2
    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)


def main():
    
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
