import time
import sys
#a = 8
"""                                                 UTILISATION
Importez le module texte. Puis utilisez l'option défilement avec la ligne text.défile("ce que vous voulez")
ATTENTION : si vous voulez utilisez une variable float ou int, vous devez utilisez str(variable), example: texte.défilement("il y a", str(variable))"""
"""                                                     USE
Import the text module. Then use the Scroll option with the line of code text.defile ("what you want")
WARNING: If you want to use a float variable or int, you must use str(variable), example: text.defile ("There is", str(variable))
"""
def defile (*x):
    for phrase in x:
        #sys.stdout.write("[phrase = " + phrase + "]\n")
        for i in phrase :
            #sys.stdout.write("i = " + i + "\n")
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.05)

