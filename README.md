# 🎨 Terminal Image Renderer

A powerful Python script that enables versatile image rendering in the terminal. Whether you're aiming for a classic ASCII art, vibrant block-based pixel art, or even a simplified display using `timg`, this tool offers a unique way to view images in the terminal.

---

## 🌟 Features

- **Three Display Modes**:
  - **ASCII Mode**: Converts images into ASCII art with colorized ANSI codes.
  - **Image Mode**: Renders trimmed and resized images directly in the terminal using `timg`.
  - **Real Image Mode**: Pixel-perfect image display using colored Unicode blocks.

- **Automatic Trimming**: Remove borders of solid color (black or white) to focus on the core image content.
- **Flexible Output Options**: Choose to display directly in the terminal or save the output to a file.
- **Customizable Width**: Specify width for all modes to control how the image is scaled in the terminal.

--- 

## 🛠️ Requirements

- **Python 3.6+**
- **Libraries**: Install dependencies with the following command:
  ```bash
  pip install -r requirements.txt
  ```
- **Optional**: `timg` (for Image Mode)
  - Install `timg` on Linux:
    ```bash
    sudo apt install timg
    ```

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/terminal-image-renderer.git
   cd terminal-image-renderer
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 📖 Usage

The script can be run in three modes: `ascii`, `image`, and `real_image`. You can also specify a width and an option to save the output to a file.

### Basic Usage

```bash
python png_to_ascii_colorscript.py <mode> <image_path> [width] [save]
```

- **`mode`**: Display mode (`ascii`, `image`, or `real_image`)
- **`image_path`**: Path to the input image file
- **`width`** (optional): Width in characters (default is 100)
- **`save`** (optional): Use `save` to save the output instead of displaying it in the terminal.

### Examples

1. **ASCII Mode**: Display an ASCII art version of the image in the terminal, with a width of 80 characters.
   ```bash
   python png_to_ascii_colorscript.py ascii my_image.png 80
   ```

2. **Image Mode**: Show the image in the terminal (requires `timg`), scaled to a width of 120 characters.
   ```bash
   python png_to_ascii_colorscript.py image my_image.png 120
   ```

3. **Real Image Mode**: Display a block-based pixel representation of the image, with trimming, at 50 characters wide.
   ```bash
   python png_to_ascii_colorscript.py real_image my_image.png 50
   ```

4. **Save Output**: Save the ASCII output to a file instead of displaying it.
   ```bash
   python png_to_ascii_colorscript.py ascii my_image.png 80 save
   ```

---

## 📂 Project Structure

- **`png_to_ascii_colorscript.py`** - The main script with all three modes and display functions.
- **`requirements.txt`** - Lists the Python dependencies.
- **`.gitignore`** - Ignores temporary files, environments, and IDE-specific files.
- **`convert_and_display.sh`** - A Bash helper script to easily execute the main Python script with various options.

---

## 🎨 Display Modes Explained

### ASCII Mode
Converts each pixel to an ASCII character based on brightness, with ANSI color for enhanced readability. Ideal for a retro terminal experience!

### Image Mode
Uses `timg` to display the image in the terminal. Requires `timg` to be installed on your system.

### Real Image Mode
Displays the image with Unicode blocks (`█`), achieving a pixelated effect that retains the color and essence of the original image.

---

## 🧩 Example Images
*Showcase a few images converted to each mode here to illustrate the script’s capabilities.*
