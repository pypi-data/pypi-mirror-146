from pynput.keyboard import Key, Listener

characters="abcçdefgğhıijklmnoçprsştuüvyzwxq1234567890.,_-!+%"


password=""

class passwordInput():
    def __init__(self,passtext=""):
        self.passtext=passtext
        print(str(self.passtext),end="\r")
        self.password=""
        def on_press(key):
            if key==Key.backspace and self.password != "":
                l=len(self.password)
                self.password=self.password[:l-1]
            elif key==Key.enter:
                print("")
                global password
                password=self.password
                return False
            else:
                if str(key).replace("'","") in characters or key==Key.space:
                    if key==Key.space:
                        self.password=self.password+" "
                    else:
                        self.password=self.password+str(key).replace("'","")
            print(self.changeText2(self.password),end="\r")
            print(str(self.passtext)+self.changeText(self.password),end="\r")
        with Listener(on_press=on_press) as listener:
            listener.join()
            if listener=="":
                return ""
    def changeText(self,text):
        i=0
        returnText=""
        while i<len(text):
            returnText=returnText+"*"
            i+=1
        return returnText
    def changeText2(self,text):
        i=-20
        returnText=""
        while i<len(text):
            returnText=returnText+" "
            i+=1
        return returnText

