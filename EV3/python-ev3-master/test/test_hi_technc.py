from __future__ import print_function
import unittest

from ev3 import robot
from test import test_util
def setUpModule():
    robot.open_all_devices()
    
def tearDownModule():
    robot.close_all_devices()
class TestHiTechncSensors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
    def setUp(self):
        print ("In method", self._testMethodName)
        
    def test_hi_technc_compass(self):
        from ev3.hi_technc import HiTechncCompass

        compass = HiTechncCompass(robot.SENSOR_3, 0x02)
        print( "start compass test")
        test_util.count_down(10, lambda:print( compass.get_angle() ))

    def test_hi_technc_pir_sensor(self):
        from ev3.hi_technc import HiTechncPIRSensor

        pir_sensor = HiTechncPIRSensor(robot.SENSOR_3, 0x02)
        print( "start PIR sensor test")
        pir_sensor.set_deadband(10)
        test_util.count_down(10, lambda:print( pir_sensor.get_measurement() ))

if __name__ == '__main__':
    unittest.main()