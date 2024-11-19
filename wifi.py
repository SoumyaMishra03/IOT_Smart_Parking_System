import network
import time

# Replace these with your Wi-Fi credentials
SSID = "PESU-EC-Campus"       # Replace with your Wi-Fi SSID
PASSWORD = "PESU-EC-Campus"  # Replace with your Wi-Fi password

def connect_wifi():
    """
    Connects the Raspberry Pi Pico W to the specified Wi-Fi network.
    """
    wlan = network.WLAN(network.STA_IF)  # Set the interface to Station mode (STA_IF)
    wlan.active(True)  # Activate the Wi-Fi interface
    wlan.connect(SSID, PASSWORD)  # Connect to the Wi-Fi network
    
    # Wait until the connection is established
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)  # Wait for 1 second before trying again
    
    print("Connected to Wi-Fi")
    print("IP Address:", wlan.ifconfig()[0])  # Print the IP address of the Pico W

# Connect to Wi-Fi
connect_wifi()
