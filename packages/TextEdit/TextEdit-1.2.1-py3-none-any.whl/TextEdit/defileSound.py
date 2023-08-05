import sys
from .Sound import Point
from .Sound import Lettre
from .Sound import Espace

ponctuation = [".", "!", ";", "?", "«", "»", "-", "'", "(", ")"]
#from playsound import playsound
#from pydub import AudioSegment
#from pydub.playback import play
def defileSound (*x):
    for phrase in x:
        #sys.stdout.write("[phrase = " + phrase + "]\n")
        for i in phrase :
            #sys.stdout.write("i = " + i + "\n")
            sys.stdout.write(i)
            sys.stdout.flush()
            if i in ponctuation :
                Point()
            elif i == " ":
                Espace()        
            else :
                Lettre()