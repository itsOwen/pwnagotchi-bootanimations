# Makefile for Pwnagotchi Boot Animation Mod

# Source files
LAUNCHER_SRC = pwnagotchi-launcher
ANIMATION_SCRIPT_SRC = boot_animation.py

# Destination paths
LAUNCHER_DEST = /usr/bin/pwnagotchi-launcher
ANIMATION_SCRIPT_DEST = /usr/local/bin/boot_animation.py
ANIMATION_IMAGES_DIR = /usr/local/bin/boot_animation_images

# Commands
INSTALL = install
CP = cp
RM = rm
MKDIR = mkdir -p

.PHONY: all install uninstall

all:
	@echo "Pwnagotchi Boot Animation Mod Installer"
	@echo "Run 'sudo make install' to install the files."
	@echo "Run 'sudo make install THEME=<folder>' to install a specific animation theme."

install:
	@echo "Backing up original pwnagotchi-launcher..."
	@if [ -f $(LAUNCHER_DEST) ] && [ ! -f $(LAUNCHER_DEST).bak ]; then \
		$(CP) $(LAUNCHER_DEST) $(LAUNCHER_DEST).bak; \
		echo "Backup created at $(LAUNCHER_DEST).bak"; \
	else \
		echo "Backup already exists or source not found, skipping backup."; \
	fi

	@echo "Injecting boot animation hook into pwnagotchi-launcher..."
	@PWN_BIN=$$(which pwnagotchi 2>/dev/null); \
	if [ -n "$$PWN_BIN" ]; then \
		REAL_LAUNCHER=$$(readlink -f "$$PWN_BIN"); \
		INTERPRETER=$$(head -n 1 "$$REAL_LAUNCHER" | sed 's/^#!//'); \
	elif [ -f "/home/pi/.pwn/bin/python3" ]; then \
		INTERPRETER="/home/pi/.pwn/bin/python3"; \
	else \
		INTERPRETER="python3"; \
	fi; \
	echo "  Using interpreter: $$INTERPRETER"; \
	if grep -q "Start of the Boot animation hook" $(LAUNCHER_DEST); then \
		echo "  Hook already present, skipping injection."; \
	else \
		TMP_HOOK=$$(mktemp); \
		echo "# Start of the Boot animation hook" > $$TMP_HOOK; \
		echo "if [ -f \"/usr/local/bin/boot_animation.py\" ]; then" >> $$TMP_HOOK; \
		echo "    $$INTERPRETER /usr/local/bin/boot_animation.py" >> $$TMP_HOOK; \
		echo "fi" >> $$TMP_HOOK; \
		echo "# End of the Boot animation hook" >> $$TMP_HOOK; \
		sed -i "/source \/usr\/bin\/pwnlib/r $$TMP_HOOK" $(LAUNCHER_DEST); \
		rm $$TMP_HOOK; \
		echo "  Hook injected successfully."; \
	fi

	@echo "Installing boot_animation.py..."
	$(INSTALL) -m 755 $(ANIMATION_SCRIPT_SRC) $(ANIMATION_SCRIPT_DEST)

	@echo "Creating default animation images directory..."
	$(MKDIR) $(ANIMATION_IMAGES_DIR)

	@if [ -n "$(THEME)" ]; then \
		if [ -d "$(THEME)" ]; then \
			echo "Installing theme from '$(THEME)'..."; \
			echo "Clearing existing animation images..."; \
			$(RM) -rf $(ANIMATION_IMAGES_DIR); \
			$(MKDIR) $(ANIMATION_IMAGES_DIR); \
			$(CP) -r "$(THEME)/." $(ANIMATION_IMAGES_DIR)/; \
			echo "Theme installed successfully."; \
		else \
			echo "Warning: Theme directory '$(THEME)' not found. Skipping theme installation."; \
		fi; \
	fi

	@echo "Locating pwnagotchi directory..."
	@PWN_BIN=$$(which pwnagotchi 2>/dev/null); \
	if [ -n "$$PWN_BIN" ]; then \
		REAL_LAUNCHER=$$(readlink -f "$$PWN_BIN"); \
		INTERPRETER=$$(head -n 1 "$$REAL_LAUNCHER" | sed 's/^#!//'); \
	else \
		INTERPRETER="/home/pi/.pwn/bin/python3"; \
	fi; \
	echo "  Interpreter: $$INTERPRETER"; \
	if [ -x "$$INTERPRETER" ]; then \
		PWN_DIR=$$("$$INTERPRETER" -c "import pwnagotchi,inspect,os; print(os.path.dirname(inspect.getfile(pwnagotchi)))"); \
		echo "  Pwnagotchi dir: $$PWN_DIR"; \
		if [ -f /etc/pwnagotchi/config.toml ]; then \
			echo "Checking display configuration..."; \
			"$$INTERPRETER" -c "import toml; c = toml.load('/etc/pwnagotchi/config.toml'); ui = c.get('ui', {}).get('display', {}); print(f'  Display Type: {ui.get(\"type\", \"N/A\")}'); print(f'  Display Rotation: {ui.get(\"rotation\", \"N/A\")}')" || echo "  Warning: Could not parse config.toml"; \
		else \
			echo "  Warning: /etc/pwnagotchi/config.toml not found."; \
		fi; \
	else \
		echo "  Warning: Python interpreter not found at $$INTERPRETER"; \
	fi

	@echo "Installation complete."

uninstall:
	@echo "Removing boot_animation.py..."
	$(RM) -f $(ANIMATION_SCRIPT_DEST)
	@if [ -f $(LAUNCHER_DEST).bak ]; then \
		echo "Restoring original pwnagotchi-launcher..."; \
		$(CP) $(LAUNCHER_DEST).bak $(LAUNCHER_DEST); \
	fi