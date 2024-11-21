import serial
from pynput.keyboard import Controller, Key
import logging
import sys

# Set up logging to capture errors
logging.basicConfig(
    filename='error.log',  # The file where the log will be saved
    level=logging.DEBUG,   # Capture all levels of logs (DEBUG, INFO, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

keyboard = Controller()

key_map = {
    "F13": Key.media_play_pause,
    "F14": Key.f14,
    "F15": Key.f15,
    "F16": Key.f16,
    "F17": Key.f17,
    "F18": Key.f18,
}

# Set the COM port directly if Arduino is always on COM3
com_port = 'COM3'

# Try to connect to Arduino on COM3
try:
    ser = serial.Serial(com_port, 9600)
    print(f"Connected to {com_port}")
    logging.info(f"Connected to {com_port}")
except Exception as e:
    print(f"Error: {e}")
    logging.error(f"Error: {e}")
    sys.exit(1)

# Main loop to listen for Arduino input
while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data in key_map:
                keyboard.press(key_map[data])
                keyboard.release(key_map[data])
    except Exception as e:
        print(f"Error in loop: {e}")
        logging.error(f"Error in loop: {e}")
        break  # Break if an error occurs
