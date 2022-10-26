import threading
import model as model 
import glob
import cv2
import os
import threading
import drone_controller


#Tum goruntuleri kiyaslayan fonksiyon. Bu fonksiyon droneKayit isimli pathdeki tum goruntuleri kiyaslar
def checkImages():
    DRONE_PATH = 'goruntuler/droneKayit'
    HEDEF_PATH = 'goruntuler/hedef'
    hedef_resimler = glob.glob(HEDEF_PATH+ '/*.png')
    x = 0
    while True:
        x += 1
        drone_resimler = glob.glob(DRONE_PATH+ '/*.png')
        drone_resimler.sort()
        if len(drone_resimler) >= 1:
            for drone in drone_resimler:
                x += 1
                isFound, gelen_resimler = model.detectAllFaces(hedef_resimler, drone)
                if isFound:
                    cv2.imwrite('goruntuler/bulunanKisiler/' + "y"+ '-' + str(x)+ '.png', gelen_resimler)
                    
            for file in os.scandir(DRONE_PATH):
                os.remove(file.path)

    
if __name__ == '__main__':
    checkImages()
    t1 = threading.Thread(target = drone_controller.main)
    t2 = threading.Thread(target = checkImages)
    t1.start()
    t2.start()
