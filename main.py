from machine import Pin, PWM
from time import sleep, ticks_us, ticks_diff, localtime
import urequests  # This library is used for HTTP requests
import ujson  # JSON module for encoding payload

# Servo motor configuration
servo_pin = PWM(Pin(14))  # Servo signal to GPIO 14
servo_pin.freq(50)

# IR sensor configuration
ir_sensor = Pin(13, Pin.IN)  # IR sensor connected to GPIO 13

# Ultrasonic sensor configuration
trig = Pin(15, Pin.OUT)  # Trigger pin to GPIO 15
echo = Pin(16, Pin.IN)   # Echo pin to GPIO 16

# ThingSpeak channel configuration
THINGSPEAK_API_KEY = "E0S6D7QOKUL8Q221"  # Replace with your actual ThingSpeak Write API Key
THINGSPEAK_URL = "https://api.thingspeak.com/update?api_key=E0S6D7QOKUL8Q221&field1=0"  # Correct ThingSpeak URL

# Variable to store timestamp
last_timestamp = ""

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

def log_timestamp(event):
    """
    Log and return the timestamp when an event occurs (car passing).
    :param event: Description of the event.
    :return: The formatted timestamp as a string.
    """
    current_time = localtime()  # Get current time as a tuple (year, month, day, hour, minute, second, ...)
    timestamp = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
        current_time[0], current_time[1], current_time[2],  # Year, Month, Day
        current_time[3], current_time[4], current_time[5]   # Hour, Minute, Second
    )
    # Log the timestamp to the console
    print(f"{event} at {timestamp}")
    return timestamp  # Return the timestamp so it can be stored in a variable

def send_to_thingspeak(timestamp):
    """
    Send the timestamp to ThingSpeak.
    :param timestamp: The timestamp to send.
    """
    try:
        # Prepare the data to send (you can send more fields if needed)
        payload = {
            'api_key': 'E0S6D7QOKUL8Q221',
            'timestamp': timestamp  # Use 'field1' to store the timestamp
        }
        
        # Convert payload to JSON
        json_payload = ujson.dumps(payload)
        
        # Send the data to ThingSpeak
        response = urequests.post(THINGSPEAK_URL, data=json_payload)
        
        if response.status_code == 200:
            print("Timestamp successfully sent to ThingSpeak")
        else:
            print("Error sending data to ThingSpeak:", response.status_code)
        response.close()  # Close the response object
    except Exception as e:
        print("Error:", e)

try:
    # Initial position (servo starts at 1022)
    print("Resetting to initial position...")
    set_servo_pwm(1500)

    while True:
        # Measure distance using the ultrasonic sensor
        distance = get_distance()
        print(f"Ultrasonic Sensor Distance: {distance:.2f} cm")

        # Check if a car is parked (distance threshold: < 10 cm)
        car_parked = distance < 10
        if car_parked:
            print("Car is parked! Barricade will remain closed.")
            set_servo_pwm(1500)  # Ensure the barricade remains closed
        else:
            print("No car parked.")
            
            # Check if the IR sensor detects an object
            if ir_sensor.value() == 0:
                # IR sensor detects an object (object is present)
                print("Object detected by IR sensor, keeping barricade up...")
                set_servo_pwm(4096)  # Move servo to 4096 (up position - barricade open)
                last_timestamp = log_timestamp("Car passed (IR sensor detected)")  # Store timestamp
                send_to_thingspeak(last_timestamp)  # Send timestamp to ThingSpeak
            else:
                # IR sensor does not detect any object
                print("No object detected by IR sensor, closing barricade...")
                set_servo_pwm(1500)  # Move servo back to initial position (down position - barricade closed)

        # Check for car passing by
        if car_parked and ir_sensor.value() == 1:  # If car is parked but IR sensor no longer detects it
            last_timestamp = log_timestamp("Car left the parking spot")  # Store timestamp when car leaves
            send_to_thingspeak(last_timestamp)  # Send timestamp to ThingSpeak

        sleep(0.5)  # Check sensors every 0.5 seconds

except KeyboardInterrupt:
    print("Program interrupted")
    servo_pin.deinit()  # Disable the PWM when done
