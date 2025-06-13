import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from imutils import paths
import face_recognition
import pickle
import os

def main():
    #newuser = NewUser("alexd22")
    facereq = FaceReq()

class NewUser():
    def __init__(self,name):
        self.name = name 

        cam = PiCamera()
        cam.resolution = (512, 304)
        cam.framerate = 10#Adjusts for Picam
        rawCapture = PiRGBArray(cam, size=(512, 304))

        photo_folder="resources/face_id/"+self.name
        if not os.path.exists(photo_folder):#Makes directory
            os.makedirs(photo_folder)
        
        
        img_counter = 0

        while True:
            for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                cv2.imshow("Press Space to take a photo", image)
                rawCapture.truncate(0)
            
                k = cv2.waitKey(1)
                rawCapture.truncate(0)
                if k%256 == 27: # ESC pressed
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = photo_folder +"/image_{}.jpg".format(img_counter)
                    cv2.imwrite(img_name, image)
                    print("{} written!".format(img_name))
                    img_counter += 1#Writes picture to database
                    
            if k%256 == 27:
                print("Escape hit, closing...")
                break

        cv2.destroyAllWindows()
class Train():
        def __init__(self):  
                imagePaths = list(paths.list_images("resources/face_id"))

                knownEncodings = []
                knownNames = []

                for (i, imagePath) in enumerate(imagePaths):

                        print("[INFO] processing image {}/{}".format(i + 1,
                                len(imagePaths)))
                        name = imagePath.split(os.path.sep)[-2]
                        image = cv2.imread(imagePath)
                        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        boxes = face_recognition.face_locations(rgb,
                                model="hog")
                        encodings = face_recognition.face_encodings(rgb, boxes)
                        for encoding in encodings:
                                knownEncodings.append(encoding)#Iterates and corrects encodings
                                knownNames.append(name)

                print("[INFO] serializing encodings...")
                data = {"encodings": knownEncodings, "names": knownNames}
                f = open("resources/encodings.pickle", "wb")
                f.write(pickle.dumps(data))
                f.close()

                

if __name__ == '__main__':
    main()
