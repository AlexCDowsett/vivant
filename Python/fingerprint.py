from pyfingerprint.pyfingerprint import PyFingerprint
import hashlib
import pickle


# CONFIG
PORT = '/dev/ttyS0'
DIRECTORY = 'resources/userdata/'


def main():
    '''This function is run when the program starts.'''
    fingerprint = Fingerprint() # Creates an instance of the class Login with the tkinter window 'root' as a parameter.

class Fingerprint():
    def __init__(self, users):
        try:
            self.f = PyFingerprint(PORT, 57600, 0xFFFFFFFF, 0x00000000)

            if (self.f.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')

        
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            
        # Sync Users
        try: 
            file = open((DIRECTORY + 'fingerprint.data'), 'rb')
            self.users = pickle.load(file)
            if len(self.users) == 0:
                self.users = []
                self.delete_all()
            else:
                # Remove fingerprints from users that no longer exist
                for i in range(len(self.users)):
                    found = False
                    for j in range(len(users)):
                        if self.users[i] == users[j][0]:
                            found = True
                            break
                    if found == False:
                        self.users[i] = None
                        self.delete(i)
                        
                # Remove None values from array.
                if self.users[0] == None:
                    self.users = []
                else:
                    while self.users[len(self.users)-1] == None:
                        self.users.pop()
                        
                        
                file = open((DIRECTORY + 'fingerprint.data'), 'wb')
                pickle.dump(self.users, file)
                file.close()
                
            
        except FileNotFoundError:
            file = open((DIRECTORY + 'fingerprint.data'), 'wb')
            self.users = []
            self.delete_all()
            pickle.dump(self.users, file)
            file.close()

        
    def is_finger_present(self):
        return self.f.readImage()
    
    def enroll(self):
        if (self.f.readImage() == False):
            return False
        
        self.f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = self.f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            return self.users[positionNumber]
            
        return True


    def enroll_confirm(self, username):
        if (self.f.readImage() == False):
            return False
        
        self.f.convertImage(0x02)

        if (self.f.compareCharacteristics() == 0):
            return True

        self.f.createTemplate()

        positionNumber = self.f.storeTemplate()
        
        while len(self.users) < (positionNumber+1):
            self.users.append(None)
            
        self.users[positionNumber] = username
        file = open((DIRECTORY + 'fingerprint.data'), 'wb')
        pickle.dump(self.users, file)
        file.close()
        
        return positionNumber
        
    def search(self):
        if (self.f.readImage() == False):
            return False
        
        self.f.convertImage(0x01)

        result = self.f.searchTemplate()

        if ( result[0] == -1 ):
            return True

        return [self.users[result[0]], result[1]]
    
    def delete(self, positionNumber):
        self.f.deleteTemplate(positionNumber)
        
    def delete_all(self):
        tableIndex = self.f.getTemplateIndex(0)
        for positionNumber in range(len(tableIndex)):
            if tableIndex[positionNumber] == True:
                self.f.deleteTemplate(positionNumber)
