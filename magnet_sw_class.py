import paho.mqtt.client as mqtt
import time 
class magnet_switch_controller:
    def __init__(self,mqtt_host,port,username,password,topic):
        self.host = mqtt_host
        self.port = port 
        self.username = username
        self.password = password 
        self.topic = topic
        self.client = mqtt.Client()
        self.on_connect = self.on_connect 
    
    def init_switch_srv(self):
        self.client.username_pw_set(self.username,self.password)
        try:
            self.client.connect(self.host, self.port, 60)
        except exception as e:
            raise IOError(e)
    
    def switch_state(self,power):
        state = "on" if power==True else "off"
        self.client.publish(self.topic,state)
     
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

if __name__=="__main__":
    switch = magnet_switch_controller("192.168.0.109",1883,"homeassistant","ihiequ8awi9tooghefeebailooz0Koh0eokohfiel5eiGhiemaiquieFieras9aa","cmnd/magnet_switch/Power1")
    switch.init_switch_srv()
    switch.switch_state(True)
    time.sleep(1)
    switch.switch_state(False)
    

