#!/usr/bin/env pybricks-micropython

from rescue_line_setup import *

# robot.straight(200)
# robot.stop()

# robot.turn(90)

# if csl.color() == Color.GREEN:
#     robot.straight(lungCingoli / 2)

#     gyro_sensor.reset_angle(0)

#     robot.drive(0, -60)

#     while gyro_sensor.angle() > -89: print(gyro_sensor.angle())

#     robot.drive(0, 0)
# elif csr.color() == Color.GREEN:
#     robot.straight(lungCingoli / 2)

#     gyro_sensor.reset_angle(0)

#     robot.drive(0, 60)

#     while gyro_sensor.angle() < 89: print(gyro_sensor.angle())


#     robot.drive(0, 0)

motori = motor_max_pwrperc

#back_motor.hold()

left_motor.dc( motori )
right_motor.dc( motori )

while True:
    pass

# new_speed_l = 0
# new_speed_r = 0

# speed_r = 0
# right_speed_r = 0


# ignora = 0
# diff_l = 0
# diff_r = 0

# media_l = 0
# media_r = 0

# i = 0

# while True:
#     if i < 20:
#         i += 1
#         continue
#     else:
#         if salta_correzione == True:
#             continue
#         else:
#             speed_l = left_motor.speed()
#             speed_r = right_motor.speed()
            
            
#             if speed_l < 300 and speed_r < 300:
#                 diff_l = 300 - speed_l
#                 diff_r = 300 - speed_r

#                 new_speed_l = (300 + diff_l) 
#                 new_speed_r = (300 + diff_r) 

#                 print("Ho applicato la correzione")
#                 salta_correzione = True
#             else:
#                 new_speed_l = motori
#                 new_speed_r = motori



#             print("velocità al motore sinistro", new_speed_l)
#             print("Velocità al motore destro", new_speed_r)

#             left_motor.dc( new_speed_l )
#             right_motor.dc( new_speed_r )


# speed = 0
# while True: 
#     speed = gyro_sensor.speed()
#     print(speed)
#     if speed > 40:
#         left_motor.hold()
#         right_motor.hold()
#         quit()
#     else:
#         continue
