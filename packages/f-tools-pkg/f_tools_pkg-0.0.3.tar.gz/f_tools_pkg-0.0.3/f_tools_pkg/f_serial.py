import serial
import struct
import time
from time import sleep

class f_serial:
    def __init__(self,COMX_i,baund,stopbits):
        COMX=COMX_i
        ser = serial.Serial(COMX,baund,stopbits=2)
        if ser.is_open:
            print(COMX,"open success")
        else:
            print(COMX,"open failed")
        print(ser.stopbits)
        return ser

    def pinfo1(m):
        if m==ord('\n'):
            print("\n       ",end="")
        elif m == ord("\r"):
            pass
        else:
            print(chr(m),end="")
            
    def recv(self,serial):
        while True:
            data = serial.read(1)
            if data == "":
                continue
            else:
                break
            sleep(0.00001)
        return int.from_bytes(data,byteorder='little',signed=False)

    #接受串口数据，以二进制写入
    def write(self,serial,data):
        serial.write(data)

    def wait_head(self,serial):
        while True:
            is_a5 = self.recv(serial)
            self.pinfo1(is_a5)
            if is_a5 == 0xA5:
                if 0x5A !=self.recv(serial):
                    continue
                else:
                    break
        return 1

    def wait_headpara(self,serial,buf):
        #serial number
        buf[2] = (self.recv(serial))
        buf[3] = (self.recv(serial))

        #test type
        buf[4] = (self.recv(serial))

        #return para num
        buf[5] = (self.recv(serial))
        buf[6] = (self.recv(serial))
        return ((buf[6]<<8) + buf[5])

    def wait_result(self,serial,buf,len):
        for i in range(0,len):
            buf.append(self.recv(serial))
        

    def wait_receive(self,serial,recvdata):
        recvdata.clear()
        recvdatahead = [0xA5,0x5A,0x00,0x00,0x00,0x00,0x00]
        recvdata.extend(recvdatahead)
        self.wait_head(serial)
        r_len = self.wait_headpara(serial,recvdata)
        self.wait_result(serial,recvdata,r_len)
        #return recvdata

    def wait_receive_headpara(self,serial,recvdata):
        recvdata.clear()
        recvdatahead = [0xA5,0x5A,0x00,0x00,0x00,0x00,0x00]
        recvdata.extend(recvdatahead)
        self.wait_head(serial)
        r_len = self.wait_headpara(serial,recvdata)
        return r_len