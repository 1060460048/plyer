'''
Android Gyroscope
---------------------
'''

from plyer.facades import Gyroscope
from jnius import PythonJavaClass, java_method, autoclass, cast
from plyer.platforms.android import activity

Context = autoclass('android.content.Context')
Sensor = autoclass('android.hardware.Sensor')
SensorManager = autoclass('android.hardware.SensorManager')


class GyroscopeSensorListener(PythonJavaClass):
    __javainterfaces__ = ['android/hardware/SensorEventListener']

    def __init__(self):
        super(GyroscopeSensorListener, self).__init__()
        self.SensorManager = cast('android.hardware.SensorManager',
                    activity.getSystemService(Context.SENSOR_SERVICE))
        self.sensor = self.SensorManager.getDefaultSensor(
                Sensor.TYPE_GYROSCOPE)

        self.values = [None, None, None]

    def enable(self):
        self.SensorManager.registerListener(self, self.sensor,
                    SensorManager.SENSOR_DELAY_NORMAL)

    def disable(self):
        self.SensorManager.unregisterListener(self, self.sensor)

    @java_method('(Landroid/hardware/SensorEvent;)V')
    def onSensorChanged(self, event):
        self.values = event.values[:3]

    @java_method('(Landroid/hardware/Sensor;I)V')
    def onAccuracyChanged(self, sensor, accuracy):
        # Maybe, do something in future?
        pass


class AndroidGyroscope(Gyroscope):
    def __init__(self):
        super(AndroidGyroscope, self).__init__()
        self.bState = False

    def _enable(self):
        if (not self.bState):
            self.listener = GyroscopeSensorListener()
            self.listener.enable()
            self.bState = True

    def _disable(self):
        if (self.bState):
            self.bState = False
            self.listener.disable()
            del self.listener

    def _get_orientation(self):
        if (self.bState):
            return tuple(self.listener.values)
        else:
            return (None, None, None)

    def __del__(self):
        if(self.bState):
            self._disable()
        super(self.__class__, self).__del__()


def instance():
    return AndroidGyroscope()
