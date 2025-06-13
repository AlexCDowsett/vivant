import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import imutils
import face_recognition
import pickle
import os
from imutils.video import VideoStream
import time
from imutils import paths
from sql import log

DIRECTORY = 'resources/userdata/'
FOLDER = 'facerec/'

def main():
    cam = Camera('alexd22')
    #cam.train()
    #facereq = FaceReq()
       
 
class Camera():
    def __init__(self,name):
        self.name = name
        self.currentname = name
       

        self.cam = PiCamera()
        #self.cam.resolution = (512, 304)
        self.cam.resolution = (640, 480)
        self.cam.framerate = 30#Adjusts for Picam
        #self.rawCapture = PiRGBArray(self.cam, size=(512, 304))
        self.rawCapture = PiRGBArray(self.cam, size=(640, 480))

        self.photo_folder= DIRECTORY + FOLDER + self.name
        if not os.path.exists(self.photo_folder):#Makes directory
            os.makedirs(self.photo_folder)
       
        self.img_counter = 0
    
    def __del__(self):
        self.cam.close()
        del self.cam
        del self.rawCapture
       
    def update(self):
       for frame in self.cam.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            self.image = frame.array
            b,g,r = cv2.split(self.image)
            img = cv2.merge((r,g,b))
            #cv2.imshow("Press Space to take a photo", image)
            self.rawCapture.truncate(0)
            k = cv2.waitKey(1)
            self.rawCapture.truncate(0)
            return img
                     
    def save(self):
        img_name = self.photo_folder +"/image_{}.jpg".format(self.img_counter)
        cv2.imwrite(img_name, self.image)
        self.img_counter += 1#Writes picture to database
                     
                     
    def train(self, only_user=False):
        if only_user == True:
            imagePaths = list(paths.list_images(DIRECTORY + FOLDER + self.name))
        else:
            imagePaths = list(paths.list_images(DIRECTORY + FOLDER))
        knownEncodings = []
        knownNames = []

        for (i, imagePath) in enumerate(imagePaths):

                log("[INFO] processing image {}/{}".format(i + 1,len(imagePaths)))
                name = imagePath.split(os.path.sep)[-2]
                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb,
                        model="hog")
                encodings = face_recognition.face_encodings(rgb, boxes)
                for encoding in encodings:
                        knownEncodings.append(encoding)#Iterates and corrects encodings
                        knownNames.append(name)

        log("[INFO] serializing encodings...")
        self.data = {"encodings": knownEncodings, "names": knownNames}
        f = open((DIRECTORY + "encodings.pickle"), "wb")
        f.write(pickle.dumps(self.data))
        f.close()
       
class FaceReq():
    def __init__(self, show=False):
        self.show = show
        self.vs = VideoStream(usePiCamera=True).start()
        time.sleep(2)
        self.encodingsP = DIRECTORY + "encodings.pickle"
        self.data = pickle.loads(open(self.encodingsP, "rb").read())

    def __del__(self):
        self.vs.stop()
        del self.vs
       
    def search(self):
        frame = self.vs.read()
        if self.show == True:
            frame = imutils.resize(frame, width=500)
        boxes = face_recognition.face_locations(frame)
       
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []
        name = None
        for encoding in encodings:
           
            matches = face_recognition.compare_faces(self.data["encodings"],
                encoding)
            name = None
            if True in matches:
               
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)

           
            names.append(name)
        if self.show == True:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                cv2.rectangle(frame, (left, top), (right, bottom),
                    (0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)

            cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1)& 0xFF
        return name
       
if __name__=='__main__':
    main()
