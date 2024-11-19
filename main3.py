from machine import Pin, PWM
from time import sleep

# Configure the GPIO pin for PWM (Servo motor control)
servo_pin = PWM(Pin(14))  # Servo signal to GPIO 14
servo_pin.freq(50)        # Standard frequency for servo motors

# Configure the GPIO pin for the IR sensor
ir_sensor = Pin(13, Pin.IN)  # IR sensor connected to GPIO 13

def set_servo_pwm(pwm_value):
    """
    Move the servo to the specified PWM duty cycle.
    :param pwm_value: PWM duty cycle (between 1022 and 4096).
    """
    servo_pin.duty_u16(pwm_value)
    sleep(1)  # Allow time for the servo to reach position

try:
    # Initial position (servo starts at 1022)
    print("Resetting to initial position...")
    set_servo_pwm(1500)

    while True:
        # Check if the IR sensor detects an object
        if ir_sensor.value() == 0:
            # IR sensor detects an object (object is present)
            print("Object detected, keeping barricade up...")
            set_servo_pwm(4096)  # Move servo to 4096 (up position - barricade open)
        else:
            # IR sensor does not detect any object
            print("No object detected, closing barricade...")
            set_servo_pwm(1500)  # Move servo back to initial position (down position - barricade closed)
        
        sleep(0.5)  # Check the IR sensor status every 0.5 seconds

except KeyboardInterrupt:
    print("Program interrupted")
    servo_pin.deinit()  # Disable the PWM when done
