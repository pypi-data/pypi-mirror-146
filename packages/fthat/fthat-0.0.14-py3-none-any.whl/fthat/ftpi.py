# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 -- Michael Schaar
# All rights reserved.
#
# License: BSD License
#
"""\
Python client to communicate with a fthat on a raspberry pi.
See https://tx-pi.de/de/hat/

It uses the ``gpiozerro`` library and ``pigpio``.

Based on: https://github.com/heuer/ftdu/
"""

import os
import time
import gpiozero
from collections import namedtuple

# Set environment variables
os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'
# Set this environment to connect a remote pi.
# os.environ['PIGPIO_ADDR'] = 'ft-pi4.local'

M1_BIN1 = 5
M1_BIN2 = 6
M1_PWM1 = 13
M2_AIN1 = 23
M2_AIN2 = 22
M2_PWM0 = 18
MX_STBY = 19

O1 = M1_BIN1
O2 = M1_BIN2
O3 = M2_AIN1
O4 = M2_AIN2

_VALID_OUTPUTS = (O1, O2, O3, O4)

_VALID_MOTOR_NAMES = ("M1", "M2")

# ft HAT usage of GPIO pins on the Raspberry Pi
I1 = 12
I2 = 16
I3 = 20
I4 = 21

_VALID_INPUTS = (I1, I2, I3, I4)
_VALID_INPUTS_NAMES = ("I1", "I2", "I3", "I4")

I2C_EXT_SDA = 2
I2C_EXT_SCL = 3
I2C_INT_SDA = 0
I2C_INT_SCL = 1

TXD0 = 14
RXD0 = 15

COUNTER_EDGE_NONE = 'none'
COUNTER_EDGE_RISING = 'rising'
COUNTER_EDGE_FALLING = 'falling'
COUNTER_EDGE_ANY = 'any'

_VALID_COUNTER_MODES = (COUNTER_EDGE_NONE, COUNTER_EDGE_RISING,
                        COUNTER_EDGE_FALLING, COUNTER_EDGE_ANY)

OFF = 0
HIGH = 1
LOW = 2

MIN = OFF
MAX = 1.0


class Counter:
    def __init__(self):
        self.__value = 0

    @property
    def value(self):
        return self.__value

    def increment(self):
        self.__value += 1

    def reset(self):
        self.__value = 0


class CounterWithOverflow(Counter):
    def __init__(self, max=63):
        self.__counter_max = max
        super().__init__()
        self.__overflow_counter = Counter()

    @property
    def counter_max(self):
        return self.__counter_max

    @counter_max.setter
    def counter_max(self, max=0):
        self.__counter_max = max

    @property
    def overflow_value(self):
        return self.__overflow_counter.value

    def increment(self):
        super().increment()
        if self.value >= self.__counter_max:
            super().reset()
            self.__overflow_counter.increment()

    def reset(self):
        super().reset()
        self.__overflow_counter.reset()


class FtMotor(gpiozero.Motor):
    """\
    :param string name:
        Motor name, i.e. 'M1'. The motor name is case-insensitive.
    :param bool pwm:
        If :data:`True` (the default), the motor controller pins, allowing
        both direction and variable speed control.
        If :data:`False` allowing only direction control.

    :type encoder: FtButton or False
    :param encoder:
        If :data `False` (the default), no encoder is set.
        If :data `FtButton` i.e. I1. The input will count the rounds.
    Resolution of encoder:
        motor: 3 pulses (6 pulses when counting 0-1 and 1-0 edge) per
        round.
        gear shaft: 63.9/127.8 pulses per round.

    :param distance:
        If distance is greater then 0, the motor will break on reaching
        round at gear shaft.
        If distance is 0, the moto round infinit.
    """
    def __init__(self, name="", pwm=True, encoder=False, distance=0):
        __INTER_GREAR = 21.3
        __RAISE = 1
        __CHANGE = 2
        __EDGE = __CHANGE
        __PULSE_MOTOR = 3 * __EDGE
        __PULSES_GEAR = __INTER_GREAR * __PULSE_MOTOR

        MOTOR = namedtuple("MOTOR", "in1 in2 pwm")

        if encoder is False or isinstance(encoder, FtButton):
            self.__encoder = encoder
            if isinstance(encoder, FtButton):
                # ToDo FtButton has counter. Use it.
                self.__counter = CounterWithOverflow(max=__PULSES_GEAR)
                self.__encoder.when_pressed = self.__increment
                if __EDGE == 2:
                    self.__encoder.when_released = self.__increment
        else:
            raise ValueError(
                'Invalid encoder "{0}" use "I1, I2, I3 or I4"'
                .format(encoder))

        try:
            self.distance = distance
        except Exception as error:
            raise Exception(error)

        if isinstance(name, str) and name.upper() in _VALID_MOTOR_NAMES:
            self.__name = name.upper()
        else:
            raise ValueError(
                'Invalid motor name "{0}" use "M1" or "M2"'
                .format(name))

        if self.__name == "M1":
            motor = MOTOR(M1_BIN1, M1_BIN2, M1_PWM1)
        else:
            motor = MOTOR(M2_AIN1, M2_AIN2, M2_PWM0)

        super().__init__(
                    forward=motor.in1,
                    backward=motor.in2,
                    enable=motor.pwm,
                    pwm=pwm
                )

    def __increment(self):
        self.__counter.increment()
        if self.distance > 0:
            if self.gear_counter >= self.distance:
                self.__callback_distance()
                self.distance = 0
                self.__counter.reset()

    @property
    def gear_counter(self):
        if isinstance(self.__encoder, FtButton):
            return self.__counter.overflow_value
        return self.__encoder

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, distance=0):
        if isinstance(distance, int):
            self.__distance = distance
            self.__counter.reset()
        else:
            raise ValueError(
                'Invalid distance "{0}" use Integer'
                .format(distance))

        if distance != 0:
            self.__callback_distance = self.brake

    def __callback_distance(self):
        pass

    # ToDo May use decorator
    def forward(self, *args, **kwargs):
        distance = kwargs.pop('distance', 0)
        self.distance = distance
        super().forward(*args, **kwargs)

    def backward(self, *args, **kwargs):
        distance = kwargs.pop('distance', 0)
        self.distance = distance
        super().backward(*args, **kwargs)

    # ToDo Motor run a litlt if init class.
    def stop(self):
        self.enable_device.off()
        super().stop()
        self.enable_device.on()

    def brake(self):
        self.enable_device.off()
        if not self.forward_device.is_active:
            self.forward_device.on()
        if not self.backward_device.is_active:
            self.backward_device.on()
        self.enable_device.on()


class FtButton(gpiozero.Button):
    def __init__(self, *args, **kwargs):
        self.counter = Counter()
        super().__init__(*args, **kwargs)
        self.when_pressed = self.counter.increment


class Inputs(gpiozero.CompositeDevice):
    def __init__(self):
        super().__init__(
            I1=FtButton(I1, pull_up=None, active_state=False),
            I2=FtButton(I2, pull_up=None, active_state=False),
            I3=FtButton(I3, pull_up=None, active_state=False),
            I4=FtButton(I4, pull_up=None, active_state=False)
        )

        # Inputs never closed allways connected
        self.close = self.__close
        for _ in range(len(self) - 1):
            self[_].close = self.__close

    def __close(self):
        pass


class BaseFtTxPiHat:
    """A dummy docstring."""
    def __init__(self, host="ft-pi4.local"):
        os.environ['PIGPIO_ADDR'] = host

        self.__host = host

        # Standby allways in use, never close
        self.STBY = gpiozero.OutputDevice(MX_STBY, initial_value=1)
        self.STBY.close = self.__close

        self.inputs = Inputs()

        self.outputs = gpiozero.CompositeOutputDevice(
            M1=FtMotor(name="M1", encoder=self.inputs.I3)
        )

    def __close(self):
        pass

    @property
    def host(self):
        """A dummy docstring."""
        return self.__host

    def ultrasonic_get(self):
        """A dummy docstring."""

    def ultrasonic_enable(self, enable):
        """A dummy docstring."""


if __name__ == "__main__":
    pi = BaseFtTxPiHat()
