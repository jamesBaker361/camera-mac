import os
import time


def get_data(file_path):
    # Get the file's metadata
    file_stats = os.stat(file_path)

    # Get the creation time (in seconds since the epoch)
    creation_time = file_stats.st_ctime

    # Convert to a human-readable format
    readable_time = time.ctime(creation_time)

    print(f"{file_path} File creation time: {readable_time} in seconds: {creation_time}")

file_path = "/Users/jbaker15/Desktop/camera/imgdir_3/camera_3_image-010.jpg"
get_data(file_path)

file_path="/Users/jbaker15/Desktop/camera/imgdir_2/camera_2_image-010.jpg"
get_data(file_path)