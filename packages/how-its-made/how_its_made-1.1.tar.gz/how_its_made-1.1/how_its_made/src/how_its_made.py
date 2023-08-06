import sys
import pyttsx3
from string import capwords as capitalise

class how_its_made:
    def __init__(self, n, it="it"):
        self.title = capitalise(self.generate_title(n, it).title())
        
    def generate_title(self, n, it):
        if n == 1: s = "'s"
        else: s = " is"

        if n == 0:
            return it
            
        return "how " + self.generate_title(n - 1, it) + s + " made"

    def text_to_speech(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(self.title)
        engine.runAndWait()

if __name__ == "__main__":

    it = "it"
    depth = 10
    if len(sys.argv) > 1: depth = int(sys.argv[1])
    if len(sys.argv) > 2: it = sys.argv[2]

    how = how_its_made(depth, it)
    print(how.title)
    how.text_to_speech()