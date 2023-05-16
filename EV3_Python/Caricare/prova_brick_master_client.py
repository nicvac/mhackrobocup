#!/usr/bin/env pybricks-micropython

from rescue_line_setup import*

# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3devExt'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
extReq = NumericMailbox('extReq', client)
extDist = NumericMailbox('extDist', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
# mbox.send('hello!')
# mbox.wait()
# print(mbox.read())




while True:
    # print(light_sensor_front.color())
    # colore = light_sensor_front.color()
    # if colore == Color.GREEN:
    extReq.send(1)
    
    extDist.wait()
    
    print(extDist.read())
       


    