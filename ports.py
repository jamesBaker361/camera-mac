import subprocess
import time
import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def extract_timestamp(image_path):
    try:
        # Open the image
        image = Image.open(image_path)
        # Get EXIF data
        exif_data = image._getexif()
        if not exif_data:
            return "No EXIF data found"
        
        # Find the DateTime tag
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTime":
                return value  # This is the timestamp
        
        return "Timestamp not found in EXIF data"
    except Exception as e:
        return f"Error: {e}"




def get_camera_ports():
    try:
        # Run the gphoto2 --auto-detect command and capture the output
        result = subprocess.run(["gphoto2", "--auto-detect"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if any cameras are detected
        if result.returncode != 0:
            print("Error detecting cameras or no cameras found.")
            print(result.stderr)
            return []

        # Parse the result to extract the ports
        lines = result.stdout.strip().split("\n")
        cameras = []

        # Skip the header and iterate through the lines to get camera details
        for line in lines[2:]:
            parts = line.split("                 ")
            if len(parts) > 1:
                camera_model = parts[0]
                port = parts[1].strip()
                cameras.append(port)

        return cameras
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



from concurrent.futures import ThreadPoolExecutor

def take_photo_from_camera(port, filename):
    try:
        subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", filename], check=True)
        print(f"Photo taken from {port} and saved as {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with {port}: {e}")



def take_frame_from_camera(port, filename):
    try:
        subprocess.run(["gphoto2", "--port", port, "--capture-preview", "--filename", filename], check=True)
        timestamp=datetime.now()
        print(f"Frame taken from {port} and saved as {filename}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with {port}: {e}")

def take_multiple_frames_from_camera(port,camera_name,n_frames):
    for k in range(n_frames):
        filename=f"img_{camera_name}_{k}.jpg"
        try:
            subprocess.run(["gphoto2", "--port", port, "--capture-preview", "--filename", filename], check=True)
            timestamp=datetime.now()
            print(f"Frame taken from {port} and saved as {filename} at {timestamp}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error occurred with {port}: {e}")

def take_multiple_photos_from_camera(port,camera_name,n_frames):
    for k in range(n_frames):
        filename=f"img_{camera_name}_{k}.jpg"
        try:
            subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", filename], check=True)
            timestamp=datetime.now()
            print(f"Frame taken from {port} and saved as {filename} at {timestamp}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error occurred with {port}: {e}")


def capture_video_from_camera(port, filename, duration=2):
    try:
        # Start video capture
        print(f"Starting video capture on {port}...")
        subprocess.run(["gphoto2", "--port", port, "--capture-movie", "--filename", filename], check=True)
        print("Capture completed successfully!")
        
        # Wait for the video to capture the specified duration (in seconds)
        time.sleep(duration)
        os.rename("movie.mjpg",filename)
        
        # Stop the capture (gphoto2 will automatically stop after the command is done)
        print(f"Video capture from {port} completed, saved as {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with {port}: {e}")

ports=get_camera_ports()
with ThreadPoolExecutor() as executor:
    for n,port in enumerate(ports):
        n_frames=3
        camera_name= f"camera_{n}" #f"img_{n}_{k}.jpg"
        executor.submit(take_multiple_photos_from_camera, port, camera_name,n_frames)
            #take_frame_from_camera(port,filename)
            #time.sleep(4)
            #filename = f"camera_{n+1}_video.mp4"
        #executor.submit(capture_video_from_camera, port, filename)

    #take_photo_from_camera(port,f"img_{n}.png")


#SOMETIMES IT TIMES OUT AND YOU LITERALLY JUST NEED TI PLUG AND UNPLUG IT AGAIN which is stupid ik