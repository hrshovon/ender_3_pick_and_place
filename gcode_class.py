from audioop import mul
import serial 
import time 
class ender_controller:

    GCODE_ABSPOS = "G90"
    GCODE_RELPOS = "G91"
    GCODE_AUTOHOME = "G28"
    GCODE_MOVEXYZ = "G1"
    GCODE_GETCURPOS = "M114"
    def __init__(self,port,baud=115200):
        self.port = port 
        self.baud = baud 
        self.serObj = None 
        self.connected_state = False
    def connect(self):
        try:
            self.serObj = serial.Serial(self.port,self.baud)
            time.sleep(3)
            self.connected_state = True 
        except:
            raise IOError(f"Could not connect to {self.port}")
    def __formcmd__(self, command):
        cmd = f"{command}\r\n"
        return str.encode(cmd)
    def __sendcmd__(self, cmd_to_send,ret_response=False):
        if self.connected_state == False:
            raise IOError("Port is not connected")
        self.serObj.write(self.__formcmd__(cmd_to_send))
        time.sleep(1)
        retbuffer = []
        while True:
            line = self.serObj.readline()
            if ret_response==True:
                retbuffer.append(line)
            print(line)
            if line == b'ok\n':
                break
        if ret_response == True:
            return retbuffer
        else:
            return True
    def initprinter(self):
        self.__sendcmd__(self.GCODE_ABSPOS)
        self.__sendcmd__(self.GCODE_AUTOHOME)

    def moveprinter(self,x=-1,y=-1,z=-1,speed=2000,multiply=False):
        base_command = self.GCODE_MOVEXYZ
        mpfac = 1 
        counter = [0,0,0] 
        
        if x>-1:
            base_command = f"{base_command} X{x}"
            counter[0]=1
        if y>-1:
            base_command = f"{base_command} Y{y}"
            counter[1]=1
        if z>-1:
            base_command = f"{base_command} Z{z}"
            counter[2]=1
        if multiply == True:
            mpfac = sum(counter)
            speed = speed*mpfac
            print("Speed", speed)
        base_command = f"{base_command} F{speed}"
        self.__sendcmd__(base_command)
        x_pos, y_pos, z_pos = self.getcurrentposition()
        return x_pos, y_pos, z_pos 


    def getcurrentposition(self):
        lines = self.__sendcmd__(self.GCODE_GETCURPOS,ret_response=True)
        for line in lines:
            line = line.decode("utf8")
            if "X:" in line:
                splitted_text = line.split(" ")
                x_pos = float(splitted_text[0][2:])
                y_pos = float(splitted_text[1][2:])
                z_pos = float(splitted_text[2][2:])
                return x_pos, y_pos, z_pos 
if __name__ == "__main__":
    controllerObj = ender_controller("/dev/ttyUSB0",115200)
    controllerObj.connect()

    controllerObj.initprinter()
    controllerObj.moveprinter(z=15,speed=8000,multiply=True)
    #controllerObj.moveprinter(x=100,y=90,speed=8000,multiply=True)
    #controllerObj.moveprinter(x=150,y=160,speed=8000,multiply=True)
    #controllerObj.moveprinter(x=10,y=30,speed=8000,multiply=True)
    #controllerObj.moveprinter(x=100,y=100,speed=8000,multiply=True)
    #controllerObj.moveprinter(x=50,y=50,speed=8000,multiply=True)
    
    
    
