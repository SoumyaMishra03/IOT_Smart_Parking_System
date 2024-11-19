from machine import Pin, PWM
from time import sleep

# Configure the GPIO pin for PWM
servo_pin = PWM(Pin(14))
servo_pin.freq(50)

def set_servo_pwm(pwm_value):
    """
    Move the servo to the specified PWM duty cycle.
    :param pwm_value: PWM duty cycle (between 1022 and 4096).
    """
    servo_pin.duty_u16(pwm_value)
    sleep(1)  # Allow time for the servo to reach position

try:
    # Move servo to 1022 (initial position)
    # print("Resetting to initial position...")
    # set_servo_pwm(1022)

    # # Move servo down to 2048 (moving downward)
    # print("Moving down to 2048...")
    # set_servo_pwm(2048)

    # # Move servo up to 3072 (moving upward)
    # print("Moving up to 3072...")
    # set_servo_pwm(3072)

    # Move servo up to 4096 (maximum position)
    print("Moving up to 4096...")
    set_servo_pwm(4096)

    # Return to initial position (1022)
    print("Returning to initial position...")
    set_servo_pwm(1500)

    # Deinitialize PWM after motion
    servo_pin.deinit()
    print("Task complete.")

except KeyboardInterrupt:
    print("Program interrupted")
    servo_pin.deinit()  # Disable the PWM when done
