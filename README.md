# 🐾 Adding a Boot Animation to Pwnagotchi

![Bootanimation-Militech](assets/militech-anim.gif)

Special thanks to [RasTacsko](https://github.com/RasTacsko) for Militech Boot animation: (Screen used: waveshare oled/lcd)

![Bootanimation](https://i.postimg.cc/bJxT8R64/tpmvhmsawvgd1.png)

This repository contains a modification for Pwnagotchi that enables custom boot animations. It modifies the default launcher to inject a Python script that plays an animation on the e-ink/OLED display before the main Pwnagotchi interface loads.  

Now you can add boot animations to your Pwnagotchi! I created this project while building a Cyberpunk-themed Pwnagotchi for myself. I will be releasing a complete set as soon as it's finished. This guide will walk you through the process step-by-step.  

![Arasaka](arasaka/frame002.png)
![umbrellacorp](umbrellacorp/frame002.png)

## Prerequisites

- 🐧 Pwnagotchi setup on Raspberry Pi
- 📟 A Supported Screen, list can be found [here](https://github.com/jayofelony/pwnagotchi/tree/master/pwnagotchi/ui/hw)
- 🔐 SSH access to your Pwnagotchi device
- Tested on Jays image

## Instructions

### 1. SSH into Your Pwnagotchi

Open a terminal and SSH into your Pwnagotchi device:

```bash
ssh pi@ip_address
```

### 2. Clone the Repository
Connect to your Pwnagotchi via SSH and clone this repository:

```bash
git clone https://github.com/itsOwen/pwnagotchi-bootanimations.git
cd pwnagotchi-bootanimations
```

### 3. Install the Mod
You can install the mod using the included `Makefile`. This will back up your existing launcher and install the necessary files.

**Standard Installation (Default Animation):**
```bash
sudo make install
```

**Installation with a Specific Theme:**
If you have a folder containing your animation images (e.g., inside a `themes` folder), you can install it directly:
```bash
sudo make install THEME=militech
# or any custom path
# sudo make install THEME=./themes/cyberpunk
```
*Note: The theme folder should contain image files (png, jpg, bmp) or a gif.*

### 4. Restart Pwnagotchi

Restart Pwnagotchi to apply the changes:

```bash
sudo systemctl restart pwnagotchi
```

### 5. Uninstall
To remove the boot animation and restore the original launcher:
```bash
sudo make uninstall
```

## How It Works

### The `boot_animation.py` Script
This Python script is responsible for rendering the animation. Here is what it does:
1.  **Configuration Loading**: It loads the Pwnagotchi configuration (`/etc/pwnagotchi/config.toml`) to understand the environment.
2.  **Display Initialization**: It dynamically initializes the correct display driver (e.g., Waveshare v2, v3, v4, Inky, etc.) based on your configuration, ensuring compatibility with whatever hardware you are using.
3.  **Image Processing**: It looks for images in `/usr/local/bin/boot_animation_images`. It supports both GIF files (extracting frames automatically) and sequences of static images. It resizes and rotates them to match your display's geometry.
4.  **Cleanup**: After the animation finishes (or if an error occurs), it cleanly disables the display driver. This prevents conflicts when the main Pwnagotchi process tries to take control of the screen.

### The `Makefile`
The Makefile automates the installation process to ensure safety and ease of use:
1.  **Backup**: It creates a backup of your original `/usr/bin/pwnagotchi-launcher` to `/usr/bin/pwnagotchi-launcher.bak` before making changes.
2.  **Interpreter Detection**: It attempts to locate the correct Python interpreter. It checks for the system `pwnagotchi` binary or the specific virtual environment path (`/home/pi/.pwn/bin/python3`) often used in custom images (like Jay's).
3.  **Launcher Patching**: It injects a startup hook directly into your existing `pwnagotchi-launcher`. This ensures compatibility with other mods and preserves your original launcher logic.
4.  **Theme Management**: If the `THEME` variable is provided, it clears the destination image directory and copies your new theme files there.
5.  **Diagnostics**: It runs a quick check at the end to verify it can load the Pwnagotchi libraries and read the display configuration.

## Troubleshooting

If the animation does not play:
1. Check the logs at `/var/log/bootanim.log`.
2. Ensure your display is correctly configured in `/etc/pwnagotchi/config.toml`.
3. Verify that images exist in `/usr/local/bin/boot_animation_images`.

## 🎥 Boot Animation Showcase

https://www.reddit.com/r/pwnagotchi/comments/1ej5fsl/cyberpunk_rebecca_x_pwnagotchi_update_1/

Feel free to replace these placeholders with actual frames from your boot animation to give a visual preview.

Enjoy your new boot animation! 🎉 Your Pwnagotchi is now even more personalized and stylish.

## 🖼️ Creating Your Own Boot Animations with Photoshop

### 1. Create a New Project

- Open Photoshop and create a new project.
- If you don't have photoshop use [Photopea](https://photopea.com/)
- Set the dimensions to match your screen resolution (e.g., 250x122 pixels for Waveshare 2.13 V4).

### 2. Design Your Animation Frames

- Design each frame of your animation.
- Make the color of the image black and white which can be done using photoshop with one click, adjust the level of darkness according to yourself.
- Keep each frame as a separate layer or save each frame as a separate file.
- Ensure the background is black or white.

### 3. Export Frames

- Export each frame as a PNG file.
  - Go to `File > Export > Export As`.
  - Choose PNG as the format.
  - Save each frame with a sequential naming convention (e.g., frame001.png, frame002.png, etc.).

### 4. Transfer Frames to Pwnagotchi

- Transfer the exported frames to your Pwnagotchi device using the SCP command provided in step 2 above.

### 5. Update Boot Animation Script

- Ensure the `boot_animation.py` script points to the directory containing your new frames.

### 6. Test and Refine

- Run the boot animation script to test your animation.
- Refine your frames in Photoshop as needed and re-export until you achieve the desired effect.

By following these steps, you can create and implement custom boot animations to give your Pwnagotchi a unique and personalized touch.
