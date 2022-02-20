# Import all board pins.
import time
import board
import bitbangio
import busio

# Import the HCSR04 ultrasonic sensor module.
import adafruit_hcsr04
# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix

# Set up the ultrasonic sensor using a library
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP2, echo_pin=board.GP3)

# Create the I2C interface for the LED
i2c = bitbangio.I2C(board.GP27, board.GP26)

# Create the matrix class
# This creates a 8x8 matrix:
matrix = matrix.Matrix8x8(i2c)

def square(min, max):
    for row in range(min,max+1):
        matrix[row, min] = 1
        matrix[row, max] = 1
    for col in range(min,max+1):
        matrix[min, col] = 1
        matrix[max, col] = 1

state = 1
while True:
    try:
        # Take a reading of the range to the object in front of the sensor
        X = sonar.distance
        # Use calibration data to adjust this value
        real_dist = 1.084*(X-9.044)+10

        # Check if distance is below 47cm
        if (real_dist < 47):
            # Calculate a blinking rate based on the distance
            rate = 5*(47 - real_dist)
            delay = min(0.2, 60 / (4*rate))
            if (state == 1):
                matrix.fill(0)
                square(3,4)
            elif (state == 2):
                square(2,5)
            elif (state == 3):
                square(1,6)
            elif (state == 4):
                square(0,7)
            print((real_dist,))

            if (state == 4):
                state = 1
            else:
                state = state + 1

            time.sleep(delay)

        else:
            matrix.fill(0)
            state = 1
            delay = 0.2
            time.sleep(delay)


        print((real_dist,))

    except RuntimeError:
        print("Retrying!")

    #time.sleep(2)
