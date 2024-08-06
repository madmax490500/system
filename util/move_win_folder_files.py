import os
import shutil

def move_png_files(base_dir):
    # Iterate over all files and subdirectories in the base directory
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.jpg'):
                # Construct full file path
                file_path = os.path.join(root, file)
                # Move file to the base directory
                shutil.move(file_path, base_dir)

    # Remove empty directories after moving files
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
            except OSError:
                pass

if __name__ == "__main__":
    base_dir = r"C:\Users\jylee\Documents\ShareX\Screenshots"
    move_png_files(base_dir)
    print("PNG files have been moved successfully.")
