from machine import Pin, PWM
from time import sleep, ticks_us, ticks_diff

# Servo motor configuration
servo_pin = PWM(Pin(14))  # Servo signal to GPIO 14
servo_pin.freq(50)

# IR sensor configuration
ir_sensor = Pin(13, Pin.IN)  # IR sensor connected to GPIO 13

# Ultrasonic sensor configuration
trig = Pin(15, Pin.OUT)  # Trigger pin to GPIO 15
echo = Pin(16, Pin.IN)   # Echo pin to GPIO 16

def set_servo_pwm(pwm_value):
    """
    Move the servo to the specified PWM duty cycle.
    :param pwm_value: PWM duty cycle (between 1022 and 4096).
    """
    servo_pin.duty_u16(pwm_value)
    sleep(1)  # Allow time for the servo to reach position

def get_distance():
    """
    Measure distance using the ultrasonic sensor.
    :return: Distance in centimeters.
    """
    # Send a 10µs pulse to TRIG
    trig.value(0)
    sleep(0.000002)  # Wait for 2µs
    trig.value(1)
    sleep(0.00001)  # Wait for 10µs
    trig.value(0)
    
    # Measure the duration of the ECHO signal
    while echo.value() == 0:
        pass
    start_time = ticks_us()
    
    while echo.value() == 1:
        pass
    end_time = ticks_us()
    
    # Calculate distance (cm)
    duration = ticks_diff(end_time, start_time)
    distance = duration / 58  # Convert µs to cm
    return distance

try:
    # Initial position (servo starts at 1022)
    print("Resetting to initial position...")
    set_servo_pwm(1500)

    while True:
        # Check if the IR sensor detects an object
        if ir_sensor.value() == 0:
            # IR sensor detects an object (object is present)
            print("Object detected by IR sensor, keeping barricade up...")
            set_servo_pwm(4096)  # Move servo to 4096 (up position - barricade open)
        else:
            # IR sensor does not detect any object
            print("No object detected by IR sensor, closing barricade...")
            set_servo_pwm(1500)  # Move servo back to initial position (down position - barricade closed)

        # Measure distance using the ultrasonic sensor
        distance = get_distance()
        print(f"Ultrasonic Sensor Distance: {distance:.2f} cm")

        # Check if a car is parked (distance threshold: < 10 cm)
        if distance < 10:
            print("Car is parked!")
        else:
            print("No car parked.")
        
        sleep(0.5)  # Check sensors every 0.5 seconds

except KeyboardInterrupt:
    print("Program interrupted")
    servo_pin.deinit()  # Disable the PWM when done
