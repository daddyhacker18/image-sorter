#!/bin/bash

# configuration
APP_NAME="image-sorter"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
SCRIPT_NAME="sort_images.py"
TARGET_LINK_NAME="image-sorter"

# Ensure directories exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

echo "Installing $APP_NAME to $INSTALL_DIR..."

# Copy files
cp "$SCRIPT_NAME" "$INSTALL_DIR/"
cp "presets.json" "$INSTALL_DIR/"

# Make executable
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# Create symlink
# Remove existing link if it exists to ensure a clean update
if [ -L "$BIN_DIR/$TARGET_LINK_NAME" ] || [ -e "$BIN_DIR/$TARGET_LINK_NAME" ]; then
    rm "$BIN_DIR/$TARGET_LINK_NAME"
fi

ln -s "$INSTALL_DIR/$SCRIPT_NAME" "$BIN_DIR/$TARGET_LINK_NAME"

echo "------------------------------------------------"
echo "Installation complete!"
echo "You can now run the tool from anywhere using:"
echo "  $TARGET_LINK_NAME"
echo ""
echo "Note: Ensure $BIN_DIR is in your PATH."
echo "------------------------------------------------"
