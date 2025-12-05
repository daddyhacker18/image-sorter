# Wallpaper Sorter

This repository contains a Python script to help organize your wallpaper collection based on custom resolution and aspect ratio criteria.

## Description

The `sort_images.py` script scans a specified directory (and its subdirectories) for image files. It determines the resolution and aspect ratio of each image and, if they meet the user-defined criteria, moves or copies them into a new, organized directory structure. This allows you to easily filter out wallpapers that are not suitable for your specific monitor setup (e.g., too low resolution, or incorrect aspect ratio).

## Features

*   **Custom Resolution Filtering:** Specify minimum width and height for images.
*   **Multiple Aspect Ratio Matching:** Define one or more target aspect ratios (e.g., `16:9`, `32:9`, `3:2`).
*   **Presets:** Easily load pre-configured settings for common devices (e.g., `framework16`, `g9`) via the `--preset` argument.
*   **Recursive Scanning:** Processes images across all subdirectories.
*   **Organized Output:** Creates a structured output directory with subfolders organized first by aspect ratio, and then by broad resolution categories (e.g., "FullHD", "4K", "Ultrawide").
*   **Copy or Move:** Choose to either copy files (default) or move them.
*   **Dry Run Mode:** Simulate the sorting process without making any changes to your files.
*   **Thumbnail Exclusion:** Automatically skips files with "thumbnail" in their name.

## Installation

To use this script, simply clone this repository to your local machine:

```bash
git clone https://github.com/your-username/wallpaper-sorter.git
cd wallpaper-sorter
```

Make sure you have `python3` installed. The script uses standard libraries and `file` command (which should be available on most Linux distributions).

## Usage

Run the script from your terminal using `python3 sort_images.py` followed by the desired arguments.

### Using Presets

Load settings for a specific device using the `--preset` argument. This overrides default width, height, and ratios.

```bash
python3 sort_images.py --preset framework16
```

You can combine presets with other arguments to override specific settings. Available presets are defined in `presets.json` (e.g., `framework13`, `framework16`, `g9`).

### Basic Sorting Example (Copying by Default)

To copy images that are at least `5120x1440` resolution with a `32:9` aspect ratio into a folder named `Ultrawide_Wallpapers`:

```bash
python3 sort_images.py --width 5120 --height 1440 --ratios 32:9 --dest Ultrawide_Wallpapers
```

### Moving Files

To move files instead of copying them, use the `--move` flag:

```bash
python3 sort_images.py --width 2560 --height 1600 --ratios 16:10 --dest Laptop_Wallpapers --move
```

### Multiple Aspect Ratios

You can specify multiple aspect ratios to match:

```bash
python3 sort_images.py --width 3840 --height 2160 --ratios 16:9 21:9 --dest 4K_and_Ultrawide_Screens
```

### Dry Run (Test without making changes)

To see which files would be affected without actually moving or copying anything, use the `--dry-run` flag:

```bash
python3 sort_images.py --width 1920 --height 1080 --ratios 16:9 --dry-run
```

### Full List of Arguments

*   `--preset STR`: Load settings from a preset configuration (e.g., `framework16`, `g9`). Overrides defaults.
*   `--width INT`: Minimum width in pixels (default: `2560`).
*   `--height INT`: Minimum height in pixels (default: `1440`).
*   `--ratios [RATIO ...]`: One or more target aspect ratios. Use `W:H` format (e.g., `16:9`, `32:9`) or a float (e.g., `1.77`). Default: `['16:9']`.
*   `--source STR`: Source directory to scan recursively (default: `.` - current directory).
*   `--dest STR`: Destination directory for sorted images (default: `Sorted_Images`).
*   `--move`: Use this flag to **move** files instead of copying them (copy is the default action).
*   `--dry-run`: Simulate the process without moving/copying files.

## Aspect Ratio Reference

Here are some common aspect ratios and their approximate decimal values for reference:

| Aspect Ratio | Decimal Value (approx.) | Typical Usage                                     |
| :----------- | :---------------------- | :------------------------------------------------ |
| `1:1`          | `1.0`                   | Square screens                                    |
| `5:4`          | `1.25`                  | Older monitors                                    |
| `4:3`          | `1.33`                  | Older standard monitors, some photography         |
| `3:2`          | `1.5`                   | Laptops (e.g., Surface devices), some photography |
| `16:10`        | `1.6`                   | Laptops, monitors                                 |
| `16:9`         | `1.77`                  | Standard Widescreen (HD, Full HD, 4K UHD)         |
| `18:9`         | `2.0`                   | Some mobile phones                                |
| `21:9`         | `2.33`                  | Ultrawide monitors                                |
| `32:9`         | `3.55`                  | Super Ultrawide monitors                          |

## Output Directory Structure Example

If you run `python3 sort_images.py --width 5120 --height 1440 --ratios 32:9 --dest My_Wallpapers`, the structure might look like this:

```
My_Wallpapers/
├── Ratio_32x9/
│   ├── UltraHD/ # Example: images with resolutions like 5120x1440, 7680x2160
│   │   ├── wallpaper1.jpg
│   │   └── wallpaper2.png
│   ├── 5K_and_above/ # Example: images with resolutions above UltraHD
│   │   ├── another_wallpaper.jpeg
│   │   └── awesome_image.png
│   └── ...
├── Ratio_16x9/
│   ├── FullHD/ # Example: images with resolutions like 1920x1080
│   │   ├── wallpaper_hd.jpg
│   │   └── another_hd.png
│   ├── 4K/ # Example: images with resolutions like 3840x2160
│   │   ├── wallpaper_4k.jpeg
│   │   └── image_4k.png
│   └── ...
└── ...
```

---
