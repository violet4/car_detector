"""
original setup/code credits to https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

"""
import RPi.GPIO as GPIO
import time
import numpy as np
import argparse

from config import (
    TRIG,
    ECHO,
    max_distance_cm
)

default_count = -1

def run_main():
    args = parse_cl_args()

    using_count = args.count != default_count
    count = args.count

    a = np.zeros(10)

    GPIO.setmode(GPIO.BCM)
    # print "Distance Measurement In Progress"
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)

    # print "Waiting For Sensor To Settle"
    time.sleep(2)

    # handle KeyboardInterrupt (control-C on the command line)
    try:
        i = 0
        while True:
            if using_count:
                count -= 1
                if count <= 0:
                    break
            GPIO.output(TRIG, True)

            # we don't need to check that often..
            # time.sleep(0.00001)
            time.sleep(0.01)

            GPIO.output(TRIG, False)
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()
            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            distance = round((pulse_end - pulse_start) * 17150, 2)
            if distance < max_distance_cm:
                a[i] = distance
                i += 1
                print('{:> 7.2f} {:>3.2f} {:>3.2f}'.format(distance, a.mean(), a.std()))
                i %= len(a)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise
    GPIO.cleanup()


    success = True
    return success

def parse_cl_args():
    argParser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    argParser.add_argument('-c', '--count', type=int, default=default_count)

    args = argParser.parse_args()
    return args


if __name__ == '__main__':
    success = run_main()
    exit_code = 0 if success else 1
    exit(exit_code)
