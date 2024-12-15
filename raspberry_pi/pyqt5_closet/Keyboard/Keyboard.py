import subprocess

class Keyboard():
    def __init__(self):
        self.KB_Active = False

    def KB_On(self):
        self.KB_Active = True
        subprocess.Popen(["bash", "Keyboard/KB_Start.sh"])

    def KB_Off(self):
        self.KB_Active = False
        subprocess.Popen(["bash", "Keyboard/KB_Off.sh"])
