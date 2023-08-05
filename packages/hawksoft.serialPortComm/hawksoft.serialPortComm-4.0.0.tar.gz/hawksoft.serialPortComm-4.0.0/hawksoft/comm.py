'''
Serial port communication package.

You can use this package as follows:
from hawksoft import comm
comm.start('COM1',9600)
...
frames = comm.receive()
for abyte in frames:
    deal the abyte
...
comm.send(b'\x01\x02')
...
comm.stop()
...
'''

from queue import Queue
import time,threading
import serial
import random

recQueue = Queue(maxsize=0)
sendQueue = Queue(maxsize=0)

paras=[False,'COM1',9600,False]

def start(com='COM1',baudRate= 9600,verbose = True):
    '''
    Start the communication thread.
    Paras:
        com: serial port name
        baudRate: baud Reate in bits per second.
        berbose: if the para is True, every bytes receiced and send will be shown as messages, 
                  otherwise will not be shown. The default value is True.
    '''
    paras[0] = False
    paras[1] = com
    paras[2] = baudRate
    paras[3] = verbose
    commThread.start()
    
def stop():
    '''
    Stop the communicatoon thread.
    paras: None
    '''
    paras[0] = False
    
    
def send(frames):
    '''
    Send bytes to serial port.
    params: frames is a bytes object
    return: None
    '''
    sendQueue.put(frames)
def receive():
    frames = b''
    bIfEmpyt = False
    while not bIfEmpyt:
        try:
            temp = recQueue.get(block = False)
        except(Exception):
            bIfEmpyt = True
        else:
            frames = frames + temp
    return frames      
        
def comm():
    #ser = serial.Serial(serialPort, baudRate, timeout=0) # 连接串口
    ser = serial.Serial(paras[1], paras[2], timeout=0) # 连接串口
    print("serial port opened successfully! 串口=%s ，波特率=%d\n" % (paras[1],paras[2]))
    while not paras[0]:
        #read
        recBytes = ser.read()
        if not (recBytes == b''):
            recQueue.put(recBytes)
            if paras[3] == True:
                print("received:",recBytes)
        
        # write    
        frames = b''
        bIfEmpyt = False
        while not bIfEmpyt:
            try:
                temp = sendQueue.get(block = False)
            except(Exception):
                bIfEmpyt = True
            else:
                frames = frames + temp    
        if len(frames)>0:
            ser.write(frames)
            if paras[3] == True:
                print('sent:',frames)
    ser.close()
    print('serial port closed successfully!')
        
commThread=threading.Thread(target=comm)

#
# folowing code is used for test and will be deleted after testing        
#
stopSign = [False]
def control():
    ticks = 0
    while not stopSign[0]:
        ticks =  ticks + 1
        if ticks >= 10:
            stopSign[0] = True
        else:
            time.sleep(1)
    print('bye')
        
        
def produce():
    while not stopSign[0]:
        #t = []
        #t.append(b'\x11')
        send(b"\x01a")
        time.sleep(random.randint(1,100)/300)
    print('producer stop')
def consume():
    while not stopSign[0]:
        frames = receive()
        if(len(frames)>0):
            print('receive=',frames)
        #for i in frames:
        #    for j in i:
        #        print('{:0>2X}'.format(j),end=',')
        #print('\n')
        time.sleep(random.randint(1,100)/100)
        #recQueue.task_done()
    print('consumer stop')
if __name__ == '__main__':
    controler =threading.Thread(target=control)
    t1=threading.Thread(target=produce)
    t2=threading.Thread(target=consume)
    controler.start()
    t1.start()
    t2.start()
