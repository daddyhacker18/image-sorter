import os
import subprocess
import re
import shutil
import argparse
import sys

# Default Configurations (can be overridden by args)
DEFAULT_TARGET_W = 2560
DEFAULT_TARGET_H = 1440
# Tolerance for aspect ratio comparison
RATIO_TOLERANCE = 0.1 

image_exts = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff'}

def get_resolution(filepath):
    try:
        result = subprocess.run(['file', filepath], capture_output=True, text=True)
        output = result.stdout
        parts = output.split(':', 1)
        content = parts[1] if len(parts) > 1 else output 
        matches = re.findall(r'(\d+)\s*x\s*(\d+)', content, re.IGNORECASE)
        for w_str, h_str in matches:
            w = int(w_str)
            h = int(h_str)
            if w > 0 and h > 0:
                return w, h
        return None
    except Exception:
        return None

def parse_ratio(ratio_str):
    try:
        if ':' in ratio_str:
            w, h = map(float, ratio_str.split(':'))
            return w / h
        return float(ratio_str)
    except ValueError:
        print(f"Error: Invalid ratio format '{ratio_str}'. Use 'W:H' (e.g., 16:9) or a float.")
        sys.exit(1)

def get_resolution_category(w, h):
    # Determine category based on the smaller dimension (e.g., height for landscape)
    # This handles both landscape and portrait orientations reasonably well.
    short_side = min(w, h)
    
    if short_side >= 4320: return "8K_UHD"
    if short_side >= 2160: return "4K_UHD"
    if short_side >= 1440: return "QHD_2K"
    if short_side >= 1080: return "FHD_1080p"
    if short_side >= 720:  return "HD_720p"
    return "Standard_Res"

def main():
    parser = argparse.ArgumentParser(description="Sort images based on resolution and aspect ratio.")
    parser.add_argument('--width', type=int, default=DEFAULT_TARGET_W, help=f'Minimum Width (default: {DEFAULT_TARGET_W})')
    parser.add_argument('--height', type=int, default=DEFAULT_TARGET_H, help=f'Minimum Height (default: {DEFAULT_TARGET_H})')
    parser.add_argument('--ratios', nargs='+', default=['16:9'], help='Target aspect ratios (e.g., "16:9 32:9 3:2"). Default: 16:9')
    parser.add_argument('--source', default='.', help='Source directory to scan (recursive). Default: current dir')
    parser.add_argument('--dest', default='Sorted_Images', help='Destination directory for sorted images. Default: Sorted_Images')
    parser.add_argument('--move', action='store_true', help='Move files instead of copying them (copy is default).')
    parser.add_argument('--dry-run', action='store_true', help='Simulate the process without moving/copying files.')

    args = parser.parse_args()

    target_w = args.width
    target_h = args.height
    target_ratios = [parse_ratio(r) for r in args.ratios]
    
    dest_root = args.dest
    if not args.dry_run and not os.path.exists(dest_root):
        os.makedirs(dest_root)

    print(f"Scanning '{args.source}'...")
    print(f"Criteria: Resolution >= {target_w}x{target_h}")
    print(f"Target Ratios: {args.ratios} (Tolerance: +/- {RATIO_TOLERANCE})")
    print(f"Action: {'Moving' if args.move else 'Copying'} to '{dest_root}'\n")

    count_moved = 0
    count_skipped = 0

    for dirpath, dirnames, filenames in os.walk(args.source):
        # Avoid scanning destination if it's inside source
        if os.path.abspath(dirpath).startswith(os.path.abspath(dest_root)):
            continue
        if '/.' in dirpath: continue

        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in image_exts:
                continue

            # Optional: skip thumbnails if desired? Let's keep it simple for now.
            if 'thumbnail' in filename.lower():
                continue

            filepath = os.path.join(dirpath, filename)
            res = get_resolution(filepath)

            if res:
                w, h = res
                img_ratio = w / h
                
                # Check Resolution
                is_high_res = (w >= target_w and h >= target_h)
                
                # Check Aspect Ratio (match ANY of the provided target ratios)
                is_valid_ratio = False
                matched_ratio_str = "Unknown"
                
                for i, target_r in enumerate(target_ratios):
                    if abs(img_ratio - target_r) < RATIO_TOLERANCE:
                        is_valid_ratio = True
                        matched_ratio_str = args.ratios[i].replace(':', 'x') # e.g. 16x9 for folder name
                        break
                
                if is_high_res and is_valid_ratio:
                    # Sort into subfolder based on Ratio -> Resolution Category
                    cat = get_resolution_category(w, h)
                    subfolder = os.path.join(dest_root, f"Ratio_{matched_ratio_str}", cat)
                    
                    if not args.dry_run:
                        if not os.path.exists(subfolder):
                            os.makedirs(subfolder)
                        
                        dest_path = os.path.join(subfolder, filename)
                        # Handle duplicates
                        if os.path.exists(dest_path):
                            base, ext = os.path.splitext(filename)
                            dest_path = os.path.join(subfolder, f"{base}_1{ext}")
                            
                        try:
                            if args.move: # If --move is specified, move
                                shutil.move(filepath, dest_path)
                            else: # Otherwise, copy (default)
                                shutil.copy2(filepath, dest_path)
                            print(f"[OK] {filename} -> {subfolder}")
                            count_moved += 1
                        except Exception as e:
                            print(f"[ERR] Failed to {'move' if args.move else 'copy'} {filename}: {e}")
                    else:
                        print(f"[Dry-Run] Would move {filename} ({w}x{h}) to {subfolder}")
                        count_moved += 1
                else:
                    count_skipped += 1

    print(f"\nOperation Complete. Processed {count_moved} files.")

if __name__ == "__main__":
    main()
