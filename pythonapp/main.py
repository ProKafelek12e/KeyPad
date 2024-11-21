import serial
from pynput.keyboard import Controller, Key
import logging
import sys
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Set up logging to capture errors
logging.basicConfig(
    filename='error.log',  # The file where the log will be saved
    level=logging.DEBUG,   # Capture all levels of logs (DEBUG, INFO, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s'
)
#Sound 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#Keyboard
keyboard = Controller()

key_map = {
    "bt1": Key.media_play_pause,
    "bt2": Key.f14,
    "bt3": Key.f15,
    "bt4": Key.f16,
    "bt5": Key.f17,
    "bt6": Key.f18,
}


volume_map = [
    -60.00, -54.00, -48.00, -44.00, -42.00, -40.00, -38.00, -36.00, -34.00, -33.00,
    -32.00, -31.00, -30.00, -29.00, -28.00, -27.00, -26.00, -25.00, -24.50, -24.00,
    -23.00, -22.00, -21.50, -21.00, -20.50, -20.00, -19.50, -19.00, -18.50, -18.00,
    -17.50, -17.00, -16.50, -16.00, -15.50, -15.00, -14.70, -14.30, -14.00, -13.70,
    -13.30, -13.00, -12.70, -12.30, -12.00, -11.70, -11.30, -11.00, -10.70, -10.30,
    -10.00, -9.70, -9.50, -9.30, -9.00, -8.70, -8.30, -8.10, -8.00, -7.70, -7.30,
    -7.10, -7.00, -6.70, -6.50, -6.30, -6.00, -5.70, -5.50, -5.30, -5.10, -5.00,
    -4.70, -4.50, -4.30, -4.10, -4.00, -3.70, -3.50, -3.30, -3.10, -3.00, -2.70,
    -2.60, -2.45, -2.30, -2.10, -2.00, -1.70, -1.50, -1.40, -1.30, -1.10, -0.90,
    -0.70, -0.55, -0.40, -0.30, -0.20, 0.00
]

def setVolume(value):
        index = int(value) - 1  # Assuming value is in the range 1-100
    
        if 0 <= index < len(volume_map):  # Validate index range
            volumeValue = volume_map[index]
            volume.SetMasterVolumeLevel(volumeValue,None)

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
            #buttonPress
            print("data: ",data)
            if data in key_map:
                keyboard.press(key_map[data])
                keyboard.release(key_map[data])
            #volume set
            elif data.startswith("V"):
                setVolume(int(data[1:]))
    except Exception as e:
        print(f"Error in loop: {e}")
        logging.error(f"Error in loop: {e}")
        break  # Break if an error occurs
