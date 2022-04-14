from gcode_class import ender_controller
from magnet_sw_class import magnet_switch_controller
import time
import json  
host = "192.168.0.109"
port = 1883 
username = ""
password = ""
topic = "cmnd/magnet_switch/Power1" 

printer_port = "/dev/ttyUSB0"

speed = 8000
fn = "./usnpwd.json"
def get_usnpwd(json_path):
    global username,password
    with open(json_path,"r") as f:
        jsonObj = json.load(f)
    username = jsonObj["username"]
    password = jsonObj["password"]


def main():
    printer_handler = ender_controller(printer_port)
    magnet_handler = magnet_switch_controller(host,port,username,password,topic)
    magnet_handler.init_switch_srv()
    printer_handler.connect()
    printer_handler.initprinter()
    printer_handler.moveprinter(z=15,speed=speed,multiply=True)
    printer_handler.moveprinter(x=110,y=160,speed=speed,multiply=True)
    magnet_handler.switch_state(True)
    time.sleep(1)
    printer_handler.moveprinter(x=220,y=220,speed=speed,multiply=True)
    time.sleep(0.5)
    magnet_handler.switch_state(False)
    time.sleep(0.5)
    printer_handler.moveprinter(x=150,y=150,speed=speed,multiply=True)
    

if __name__ == "__main__":
    main()
    