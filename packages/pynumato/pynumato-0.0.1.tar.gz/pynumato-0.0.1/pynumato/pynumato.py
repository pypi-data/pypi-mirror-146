import sys
import serial
import os
import argparse

class Numato(object):
    def __init__(self, *, numberRelays=1, port="COM27", baudrate=921600, timeout=1):
        self.version = 0
        self.numberRelays= numberRelays
        self.stateRelays=[0]*numberRelays
        self.port=port
        self.baudrate=baudrate
        self.timeout=timeout

        self.read_all_relays()

    def send_cmd(self, cmd, *, noResponse=True, sizeResponse=0):
        #Open port for communication
        serPort = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

        # Send command
        serPort.write(cmd.encode())

        # Get response command
        if not(noResponse):
            ret = serPort.read(sizeResponse)
            response = ret.decode('UTF-8')

        #Close the port
        serPort.close()

        if not(noResponse):
            return response

    def get_version(self):
        cmd="ver\n\r"
        response = self.send_cmd(cmd=cmd, noResponse= False, sizeResponse=25)
        #print("response=", response)
        version=int(response[len(cmd):-1])
        print("Version is", version)
        return version

    def reset(self):
        cmd="reset\n\r"
        self.send_cmd(cmd=cmd)
        print("Reset all relays")

    #----- functions for single relay -----#
    def open_single_relay(self, indexRelay):
        cmd="relay on "+ str(indexRelay) + "\n\r"
        self.send_cmd(cmd=cmd)
        self.stateRelays[indexRelay] = 1

    def close_single_relay(self, indexRelay):
        cmd="relay off "+ str(indexRelay) + "\n\r"
        self.send_cmd(cmd=cmd)
        self.stateRelays[indexRelay] = 0

    def read_single_relay(self, indexRelay):
        cmd="relay read "+str(indexRelay)+"\n\r"
        ret = self.send_cmd(cmd=cmd, noResponse= False, sizeResponse=25)
        if(ret.find("on") > 0):
            self.stateRelays[indexRelay] = 1
        elif(ret.find("off") > 0):
            self.stateRelays[indexRelay] = 0

    def get_single_relay(self,indexRelay):
        if self.stateRelays[indexRelay]:
            print("Relay " + str(indexRelay) +" is ON")
        else:
            print("Relay " + str(indexRelay) +" is OFF")
        return self.stateRelays[indexRelay]

    #----- functions for all relay -----#
    def read_all_relays(self):
        cmd="relay readall\n\r"
        response = self.send_cmd(cmd=cmd, noResponse= False, sizeResponse=25)
        #print("response=",response)
        states=int(response[len(cmd):-1])
        for i in range(0,self.numberRelays):
            if ((states >> i) & 0x01) == 0x01 :
                self.stateRelays[i]=1
            else:
                self.stateRelays[i]=0

    def open_all_relays(self):
        cmd="relay writeall ff\n\r"
        self.send_cmd(cmd=cmd)
        for i in range(0,self.numberRelays):
            self.stateRelays[i]=1

    def close_all_relays(self):
        cmd="relay writeall 0\n\r"
        self.send_cmd(cmd=cmd)
        for i in range(0,self.numberRelays):
            self.stateRelays[i]=0

    def update_all_relays(self,cmdRelay= "xxxxxxxx"):
        assert(len(cmdRelay) <= self.numberRelays)
        for idxRelay in range(len(cmdRelay)):
            if cmdRelay[idxRelay] == 'o':
                self.open_single_relay(idxRelay)
            elif cmdRelay[idxRelay] == 'c':
                self.close_single_relay(idxRelay)

def main(args=None):
    scriptname = os.path.basename(__file__)
    parser = argparse.ArgumentParser(scriptname)
    parser.add_argument('--relays', default=1, type=int)
    parser.add_argument('--port', default="/dev/ttyUSB1", type=str)
    parser.add_argument('--timeout', default=1, type=int)
    parser.add_argument('--baudrate', default=921600, type=int)
    parser.add_argument('--cmd', default="x", type=str)

    options = parser.parse_args()

    numatoRelay= Numato(numberRelays=options.relays, port=options.port, baudrate=options.baudrate, timeout=options.timeout)
    numatoRelay.update_all_relays(cmdRelay=options.cmd)

    return 0

if __name__=="__main__":
    ret=main()
    os._exit(ret)
