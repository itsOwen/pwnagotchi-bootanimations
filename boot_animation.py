import time
from PIL import Image
from pwnagotchi.ui.hw import waveshare2in13_V4  # Change this import based on your screen type
import os

class CustomWaveshareV4(waveshare2in13_V4.WaveshareV4):  # Change this based on your screen type
    def __init__(self, config):
        super().__init__(config)

    def layout(self):
        return None

    def initialize(self):
        from pwnagotchi.ui.hw.libs.waveshare.epaper.v2in13_V4.epd2in13_V4 import EPD  # Change this based on your screen type
        self._display = EPD()
        self._display.init()
        self._display.Clear(0xFF)  # Clear to white

    def render(self, canvas):
        buf = self._display.getbuffer(canvas)
        self._display.displayPartial(buf)

    def clear(self):
        self._display.Clear(0xFF)  # Clear to white

def show_boot_animation():
    config = {
        'ui': {
            'display': {
                'type': 'ws4',  # Change this based on your screen type
                'color': 'black'
            }
        }
    }
    display = CustomWaveshareV4(config)
    display.initialize()
    width, height = 250, 122  # Dimensions of the 2.13 inch display

    # Path to the boot animation frames
    frames_path = '/usr/local/bin/boot_animation_images/'

    # Ensure at least 3 loops within the 5-second duration
    min_loops = 3
    total_duration = 5
    start_time = time.time()
    loop_count = 0
    
    try:
        while (time.time() - start_time < total_duration) or (loop_count < min_loops):
            # Get all PNG files in the directory
            frames = sorted([f for f in os.listdir(frames_path) if f.endswith('.png')])
            
            for frame in frames:
                if (time.time() - start_time >= total_duration) and (loop_count >= min_loops):
                    break
                with Image.open(os.path.join(frames_path, frame)) as img:
                    img = img.resize((width, height)).transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT).convert('1')  # Resize, flip vertically and horizontally, and convert to 1-bit color
                    display.render(img)
                    time.sleep(0.167)  # Adjust this value to control animation speed
            loop_count += 1
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        display.clear()  # Only clear if an exception occurs

if __name__ == "__main__":
    show_boot_animation()