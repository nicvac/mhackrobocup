#!/usr/bin/python

from __future__ import absolute_import
from roberta.ev3 import Hal
from ev3dev import ev3 as ev3dev
import math
import os
import time

class BreakOutOfALoop(Exception): pass
class ContinueLoop(Exception): pass

_brickConfiguration = {
    'wheel-diameter': 3.0,
    'track-width': 15.0,
    'actors': {
        'A':Hal.makeLargeMotor(ev3dev.OUTPUT_A, 'on', 'foreward'),
        'B':Hal.makeLargeMotor(ev3dev.OUTPUT_B, 'on', 'foreward'),
        'C':Hal.makeMediumMotor(ev3dev.OUTPUT_C, 'on', 'foreward'),
    },
    'sensors': {
        '1':Hal.makeUltrasonicSensor(ev3dev.INPUT_1),
        '2':Hal.makeColorSensor(ev3dev.INPUT_2),
        '3':Hal.makeColorSensor(ev3dev.INPUT_3),
        '4':Hal.makeColorSensor(ev3dev.INPUT_4),
    },
}
hal = Hal(_brickConfiguration)

___counter_curve = 0
___wall_distance = hal.getUltraSonicSensorDistance('1')
___first_distance = hal.getUltraSonicSensorDistance('1')
___verdi_visti = 0
___rossi_visti = 0
___flag_scan = True
___e = 30
___curva = 0
___i = 0

def ____rilascio_rescue_kit():
    global ___counter_curve, ___wall_distance, ___first_distance, ___verdi_visti, ___rossi_visti, ___flag_scan, ___e, ___curva, ___i
    hal.driveDistance('B', 'A', False, 'foreward', 30, 20)
    hal.rotateDirectionAngle('B', 'A', False, 'left', 30, 180)

def ____rescue_kit():
    global ___counter_curve, ___wall_distance, ___first_distance, ___verdi_visti, ___rossi_visti, ___flag_scan, ___e, ___curva, ___i
    hal.driveDistance('B', 'A', False, 'backward', 30, 20)
    hal.rotateDirectionAngle('B', 'A', False, 'right', 30, 180)
    hal.driveDistance('B', 'A', False, 'backward', 30, 20)
    hal.rotateRegulatedMotor('C', 75, 'rotations', 135)
    hal.waitFor(500)
    hal.rotateRegulatedMotor('C', -75, 'rotations', 135)
    hal.waitFor(500)
    hal.rotateRegulatedMotor('C', 75, 'rotations', 135)
    hal.waitFor(500)
    hal.rotateRegulatedMotor('C', -75, 'rotations', 135)
    hal.waitFor(500)
    hal.rotateRegulatedMotor('C', 75, 'rotations', 135)
    hal.waitFor(500)
    hal.rotateRegulatedMotor('C', -75, 'rotations', 135)

def ____stanza():
    global ___counter_curve, ___wall_distance, ___first_distance, ___verdi_visti, ___rossi_visti, ___flag_scan, ___e, ___curva, ___i
    hal.waitFor(300)
    hal.driveDistance('B', 'A', False, 'foreward', 30, 10)
    hal.waitFor(1000)
    ___first_distance = hal.getUltraSonicSensorDistance('1')
    hal.rotateDirectionAngle('B', 'A', False, 'right', 30, 30)
    ___wall_distance = hal.getUltraSonicSensorDistance('1')
    hal.waitFor(1000)
    if ___wall_distance < ___first_distance:
        ___curva = -1
    else:
        ___curva = 1
    hal.rotateDirectionAngle('B', 'A', False, 'left', 30, 30)
    while True:
        hal.regulatedDrive('B', 'A', False, 'foreward', 30)
        if ( hal.getColorSensorColour('4') == 'green' ) and ( ___counter_curve == 0 ):
            ____rescue_kit()
            ____rilascio_rescue_kit()
            ___counter_curve = ___counter_curve + 1
        else:
            if ( hal.getColorSensorColour('4') == 'green' ) and ( ___counter_curve > 1 ):
                ____rescue_kit()
                ____rilascio_rescue_kit()
                hal.rotateDirectionAngle('B', 'A', False, 'right', 50 * ___curva, 180)
            else:
                if ( ( hal.getColorSensorColour('4') == 'red' ) or ( hal.getColorSensorColour('4') == 'yellow' ) ) and ( ___counter_curve == 0 ):
                    ___counter_curve = 2
                    hal.rotateDirectionAngle('B', 'A', False, 'right', 20 * ___curva, 90)
                    hal.driveDistance('B', 'A', False, 'foreward', 20, 20)
                    hal.rotateDirectionAngle('B', 'A', False, 'right', 20 * ___curva, 90)
                    ___curva = ___curva * -1
                else:
                    if ( ( hal.getColorSensorColour('4') == 'red' ) or ( hal.getColorSensorColour('4') == 'yellow' ) ) and ( ( ___counter_curve > 1 ) and ( ___verdi_visti == 0 ) ):
                        hal.rotateDirectionAngle('B', 'A', False, 'right', 20 * ___curva, 180)
                    else:
                        if ( ( hal.getColorSensorColour('4') == 'red' ) or ( hal.getColorSensorColour('4') == 'yellow' ) ) and ( ( ___counter_curve > 1 ) and ( ___verdi_visti > 0 ) ):
                            hal.driveDistance('B', 'A', False, 'backward', 30, 20)
                            break
                        else:
                            if hal.getUltraSonicSensorDistance('1') < 6:
                                hal.rotateDirectionAngle('B', 'A', False, 'right', 20 * ___curva, 90)
                                hal.driveDistance('B', 'A', False, 'foreward', 20, 20)
                                hal.rotateDirectionAngle('B', 'A', False, 'right', 20 * ___curva, 90)
                                ___curva = ___curva * -1
                                ___counter_curve = ___counter_curve + 1

def ____aggira_ostacolo():
    global ___counter_curve, ___wall_distance, ___first_distance, ___verdi_visti, ___rossi_visti, ___flag_scan, ___e, ___curva, ___i
    hal.rotateDirectionAngle('B', 'A', False, 'left', 30, 15)
    if ( hal.getColorSensorColour('2') == 'black' ) or ( hal.getColorSensorColour('3') == 'black' ):
        hal.rotateDirectionAngle('B', 'A', False, 'right', 30, 15)
        hal.driveDistance('B', 'A', False, 'backward', 20, 20)
        hal.rotateDirectionAngle('B', 'A', False, 'left', 30, 70)
        _driveInCurve('foreward', 'B', 30, 'A', 55)
        while True:
            if ( hal.getColorSensorColour('2') == 'black' ) or ( ( hal.getColorSensorColour('3') == 'black' ) or ( hal.getColorSensorRed('4') < 10 ) ):
                break
    else:
        hal.rotateDirectionAngle('B', 'A', False, 'right', 30, 30)
        if ( hal.getColorSensorColour('2') == 'black' ) or ( hal.getColorSensorColour('3') == 'black' ):
            hal.rotateDirectionAngle('B', 'A', False, 'left', 30, 15)
            hal.driveDistance('B', 'A', False, 'backward', 20, 20)
            hal.rotateDirectionAngle('B', 'A', False, 'left', 30, 70)
            _driveInCurve('foreward', 'B', 30, 'A', 55)
            while True:
                if ( hal.getColorSensorColour('2') == 'black' ) or ( ( hal.getColorSensorColour('3') == 'black' ) or ( hal.getColorSensorRed('4') < 10 ) ):
                    break
        else:
            hal.driveDistance('B', 'A', False, 'backward', 30, 30)
            ____stanza()

def ____scansione_linea():
    global ___counter_curve, ___wall_distance, ___first_distance, ___verdi_visti, ___rossi_visti, ___flag_scan, ___e, ___curva, ___i
    ___i = 0
    while not (( hal.getColorSensorColour('2') == 'blue' ) and ( ( hal.getColorSensorColour('3') == 'blue' ) and ( ( hal.getColorSensorColour('2') == 'black' ) and ( ( hal.getColorSensorColour('3') == 'black' ) and ( hal.getColorSensorRed('4') < 40 ) ) ) )):
        if ___i < 13:
            hal.rotateDirectionAngle('B', 'A', False, 'right', 60, 1)
        else:
            if ___i < 35:
                hal.rotateDirectionAngle('B', 'A', False, 'left', 60, 1)
            else:
                hal.rotateDirectionAngle('B', 'A', False, 'right', 60, 35)
                hal.driveDistance('B', 'A', False, 'foreward', 50, 2)
                ___i = 0
        ___i = ___i + 1

def run():
    global ___counter_curve, ___wall_distance, ___first_distance, ___verdi_visti, ___rossi_visti, ___flag_scan, ___e, ___curva, ___i
    while True:
        if hal.getColorSensorRed('4') >= 95:
            _driveInCurve('foreward', 'B', 30, 'A', 30, 5)
            if ( hal.getColorSensorRed('2') >= 95 ) and ( hal.getColorSensorRed('3') >= 95 ):
                ____stanza()
            else:
                ____scansione_linea()
        else:
            if ( hal.getColorSensorRed('4') <= 10 ) and ( ( hal.getColorSensorColour('2') == 'black' ) and ( hal.getColorSensorColour('3') == 'black' ) ):
                hal.driveDistance('B', 'A', False, 'foreward', 30, 5)
                ___flag_scan = True
            else:
                if ( hal.getColorSensorColour('2') == 'black' ) or ( hal.getColorSensorColour('2') == 'blue' ):
                    _driveInCurve('foreward', 'B', -40, 'A', 50)
                    ___flag_scan = True
                else:
                    if ( hal.getColorSensorColour('3') == 'black' ) or ( hal.getColorSensorColour('3') == 'blue' ):
                        _driveInCurve('foreward', 'B', 50, 'A', -40)
                        ___flag_scan = True
                    else:
                        if ( hal.getColorSensorColour('3') == 'black' ) or ( hal.getColorSensorColour('3') == 'blue' ):
                            _driveInCurve('foreward', 'B', 50, 'A', -40)
                            ___flag_scan = True
                        else:
                            if ( hal.getColorSensorColour('2') == 'green' ) and ( hal.getColorSensorColour('3') == 'green' ):
                                hal.rotateDirectionAngle('B', 'A', False, 'right', 50, 180)
                            else:
                                if hal.getColorSensorColour('2') == 'green':
                                    _driveInCurve('foreward', 'B', -20, 'A', 60, 10)
                                else:
                                    if hal.getColorSensorColour('3') == 'green':
                                        _driveInCurve('foreward', 'B', 60, 'A', -20, 10)
                                    else:
                                        if ( hal.getColorSensorColour('2') == 'white' ) and ( ( hal.getColorSensorColour('3') == 'white' ) and ( ( hal.getColorSensorRed('4') > 50 ) and ( hal.getColorSensorRed('4') < 90 ) ) ):
                                            if ___flag_scan == True:
                                                ____scansione_linea()
                                        else:
                                            if hal.getUltraSonicSensorDistance('1') < 5:
                                                ____aggira_ostacolo()
                                            else:
                                                hal.regulatedDrive('B', 'A', False, 'foreward', 40)

def main():
    try:
        run()
    except Exception as e:
        hal.drawText('Fehler im EV3', 0, 0)
        hal.drawText(e.__class__.__name__, 0, 1)
        hal.drawText(str(e), 0, 2)
        hal.drawText('Press any key', 0, 4)
        while not hal.isKeyPressed('any'): hal.waitFor(500)
        raise

def _busyWait():
    time.sleep(0.0)

def _clamp(v, mi, ma):
    return mi if v < mi else ma if v > ma else v

def _driveInCurve(direction, left_port, left_speed_pct, right_port, right_speed_pct, distance=None):
    # direction: foreward, backward
    ml = _brickConfiguration['actors'][left_port]
    mr = _brickConfiguration['actors'][right_port]
    left_speed_pct = _scaleSpeed(ml, _clamp(left_speed_pct, -100, 100))
    right_speed_pct = _scaleSpeed(mr, _clamp(right_speed_pct, -100, 100))
    if distance:
        left_dc = right_dc = 0.0
        speed_pct = (left_speed_pct + right_speed_pct) / 2.0
        if speed_pct:
            circ = math.pi * _brickConfiguration['wheel-diameter']
            dc = distance / circ
            if direction == 'backward':
                dc = -dc
            left_dc = dc * left_speed_pct / speed_pct
            right_dc = dc * right_speed_pct / speed_pct
        # set all attributes
        ml.stop_action = 'brake'
        ml.speed_sp = int(left_speed_pct)
        mr.stop_action = 'brake'
        mr.speed_sp = int(right_speed_pct)
        ml.position_sp = int(left_dc * ml.count_per_rot)
        mr.position_sp = int(right_dc * mr.count_per_rot)
        # start motors
        ml.run_to_rel_pos()
        mr.run_to_rel_pos()
        while ((ml.state and left_speed_pct) or (mr.state and right_speed_pct)):
            _busyWait()
    else:
        multiplier = -1 if direction == 'backward' else 1
        ml.run_forever(speed_sp = multiplier * int(left_speed_pct))
        mr.run_forever(speed_sp = multiplier * int(right_speed_pct))

def _scaleSpeed(m, speed_pct):
    return int(speed_pct * m.max_speed / 100.0)

if __name__ == "__main__":
    main()