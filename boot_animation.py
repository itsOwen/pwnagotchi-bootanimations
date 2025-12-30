import time
from PIL import Image, ImageSequence
import os
import logging
from pwnagotchi import utils
import pwnagotchi.ui.hw as hw

from pwnagotchi.ui.hw import display_for
import argparse
#import traceback

def setup_logging(log_file='/var/log/bootanim.log'):
    # Ensure the directory exists
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure logging
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,  # or DEBUG, WARNING, ERROR, CRITICAL
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def get_display_geometry(display):
    cfg = getattr(display, 'config', {})
    width = getattr(display, 'width', None) or cfg.get('width')
    height = getattr(display, 'height', None) or cfg.get('height')
    rotation = cfg.get('rotation', 0)
    return width, height, rotation

def show_boot_animation(display_driver, config):
    try:
        frames_path = '/usr/local/bin/boot_animation_images/'
        width, height, rotation = get_display_geometry(display_driver)
        
        # Fallbacks
        width = width or 320
        height = height or 240
        rotation = rotation or 0

        # Check if folder exists
        if not os.path.exists(frames_path):
            return

        # Accept common image formats
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        frames = sorted([f for f in os.listdir(frames_path) if f.lower().endswith(valid_extensions)])
        logging.debug("Found %s frames" % len(frames))
        # Check if there are any images to process
        if not frames:
            return

        frames_count = len(frames)

        if len(frames) == 1:
            if frames[0].lower().endswith('.gif'):
                source_path = os.path.join(frames_path, frames[0])
                with Image.open(source_path) as img:
                    frames_count = sum(1 for _ in ImageSequence.Iterator(img))

        max_loops = 1
        total_duration = 2
        start_time = time.time()
        loop_count = 0

        delay =  total_duration / (frames_count * max_loops)

        while (time.time() - start_time < total_duration) or (loop_count < max_loops):
            for frame in frames:
                if (time.time() - start_time >= total_duration) and (loop_count >= max_loops):
                    break
                
                frame_path = os.path.join(frames_path, frame)

                if rotation in (90, 270):
                    target_size = (height, width)
                else:
                    target_size = (width, height)

                if frame.lower().endswith('.gif'):
                    logging.debug('Processing GIF: %s' % frame_path)
                    with Image.open(frame_path) as img:
                        for gif_frame in ImageSequence.Iterator(img):
                            gif_frame = gif_frame.resize(target_size)
                            if rotation:
                                gif_frame = gif_frame.rotate(rotation, expand=True)
                            gif_frame = gif_frame.convert('P')
                            logging.debug('Rendering frame: %s' % gif_frame)
                            display_driver.render(gif_frame)
                else:
                    # Handle any other image formats (jpg, jpeg, bmp, png, etc.)
                    with Image.open(frame_path) as img:
                        img = img.resize(target_size)
                        if rotation:
                            img = img.rotate(rotation, expand=True)
                        img = img.convert('P')
                        logging.debug('Rendering frame: %s' % img)
                        display_driver.render(img)
                        
                time.sleep(delay)  # Adjust this value to control animation speed
            logging.debug('Finished loop %d' % loop_count)
            loop_count += 1
            
    except Exception as ex:
        logging.error(ex)
        #logging.error(traceback.format_exc())
        display_driver.clear()

if __name__ == "__main__":
    setup_logging()
    logging.debug('Starting boot animation...')
    args = argparse.Namespace(
        config='/etc/pwnagotchi/default.toml', 
        user_config='/etc/pwnagotchi/config.toml', 
        do_manual=False, 
        skip_session=False, 
        do_clear=False, 
        debug=False, 
        version=False, 
        print_config=False, 
        wizard=False, 
        check_update=False, 
        donate=False
    )
    logging.debug(args)
    try:
        config = utils.load_config(args)
        logging.debug('Display config: %s' % config['ui']['display'])
        logging.debug('Display type: %s' % config['ui'])
        display_type = config['ui']['display']['type']
        logging.debug('Display type: %s' % display_type)
        display_driver = display_for(config)
        logging.debug(vars(display_driver))
        if display_driver is not None:
            
            if hasattr(display_driver, 'initialize'):
                try:
                    display_driver.initialize()
                    show_boot_animation(display_driver, config)
                    display_driver.config['enabled'] = True
                    display_driver.is_initialized = True
                except Exception as e:
                    logging.error(e)
            display_driver.config['enabled'] = False

            if hasattr(display_driver, 'displayImpl') and display_driver.config.get('enabled', False):
                display_driver.config['enabled'] = False
                logging.debug('[Fancygotchi] Display has been disabled')
                
                if hasattr(display_driver, 'clear'):
                    logging.debug('[Fancygotchi] Clearing the display')
                    display_driver.clear()
                
                display_driver.is_initialized = False

                if hasattr(display_driver, '_display'):
                    logging.debug('[Fancygotchi] Resetting internal display reference')
                    display_driver._display = None
        else:
            logging.error("Failed to initialize the display driver.")
    except KeyError as e:
        logging.error('KeyError: %s' % e)
        #logging.error(traceback.format_exc())
        display_type = 'Unknown'
