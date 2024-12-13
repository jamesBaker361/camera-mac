import subprocess
import time
import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import threading

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
    #print("called fucntion with  ",camera_name)
    files_in_dir = os.listdir()

# Check if any file contains the substring
    file_exists = any(camera_name in filename for filename in files_in_dir)
    if file_exists:
        return
    for k in range(n_frames):
        filename=f"img_{camera_name}_{k}.jpg"
        try:
            subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", filename], check=True)
            timestamp=datetime.now()
            print(f"Frame taken from {port} and saved as {filename} at {timestamp}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error occurred with {port}: {e}")


def capture_video_from_camera(port, filename, duration,cwd):
    try:
        # Start video capture
        print(f"Starting video capture on {port}...")
        subprocess.run(["gphoto2", "--port", port, "--capture-movie", "--filename", filename, ], check=True,cwd=cwd)
        print("Capture completed successfully!")
        
        # Wait for the video to capture the specified duration (in seconds)
        time.sleep(duration)
        os.rename("movie.mjpg",filename)
        
        # Stop the capture (gphoto2 will automatically stop after the command is done)
        print(f"Video capture from {port} completed, saved as {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with {port}: {e}")

def capture_video_from_camera_event(start_event,port, filename, duration,cwd):
    start_event.wait()
    start=time.time()
    print(cwd," video starting at ",start)
    try:
        # Start video capture
        print(f"Starting video capture on {port}...")
        subprocess.run(["gphoto2", "--port", port, "--capture-movie",str(duration), "-I","1"], check=True,cwd=cwd)
        print("Capture completed successfully!")
        
        # Wait for the video to capture the specified duration (in seconds)
        #time.sleep(duration)
        #os.rename("movie.mjpg",filename)
        
        # Stop the capture (gphoto2 will automatically stop after the command is done)
        print(f"Video capture from {port} completed, saved as {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with {port}: {e}")

def take_multiple_photos_from_camera_with_event(start_event,step,port,camera_name,n_frames,cwd):
    #print("called fucntion with  ",camera_name)
    files_in_dir = os.listdir()

# Check if any file contains the substring
    file_exists = any(camera_name in filename for filename in files_in_dir)
    if file_exists:
        return
    
    start_event.wait()
    start=time.time()
    print(camera_name," starting at ",start)
    command=["gphoto2", "--port", port, "--capture-image-and-download", "--filename", camera_name+"_image-%03n.jpg","--force-overwrite" , f"--frames={n_frames}","--interval=2"]
    command.append(["--debug" ,f"--debug-logfile=gphoto-debug-{camera_name}.log"])
    subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", camera_name+"_image-%03n.jpg","--force-overwrite" , f"--frames={n_frames}","--interval=2","--debug" ,f"--debug-logfile=gphoto-debug-{camera_name}.log","--wait-event=2s"],cwd=cwd)
    print(f"Frame taken from {port} and saved as {camera_name} at {time.time()}")
    '''while n_frames>0:
        now=time.time()
        if now>=start:
            start+=step
            filename=f"img_{camera_name}_{n_frames}.jpg"
            try:
                print(f"{camera_name} beginning photo {n_frames} at {time.time()}")
                subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", filename, "-q","--force-overwrite"],cwd=cwd)
                timestamp=datetime.now()
                #print(f"Frame taken from {port} and saved as {filename} at {timestamp}")
                
            except subprocess.CalledProcessError as e:
                print(f"Error occurred with {port}: {e}")
            n_frames-=1'''
if __name__=="__main__":
    '''threads=[]
    start_event = threading.Event()
    ports=get_camera_ports()
    for n,port in enumerate(ports):
        
        filename= f"camera_{n}.mp4" #f"img_{n}_{k}.jpg"
        cwd=f"imgdir_{n}"
        os.makedirs(cwd,exist_ok=True)
        threads.append(threading.Thread(target=capture_video_from_camera_event,args=(start_event,port,filename,10,cwd)))
    for t in threads:
        t.start()
    time.sleep(1)
    start_event.set()'''
    #subprocess.run(["gphoto2", "--reset"])
    start_event = threading.Event()
    step=0.5
    ports=get_camera_ports()
    #with ThreadPoolExecutor() as executor:
    threads=[]
    for n,port in enumerate(ports):
        cwd=f"imgdir_{n}"
        os.makedirs(cwd,exist_ok=True)
        n_frames=3
        camera_name= f"camera_{n}" #f"img_{n}_{k}.jpg"
        #executor.submit(take_multiple_photos_from_camera_with_event, start_event, step, port, camera_name,n_frames)
        threads.append(threading.Thread(target=take_multiple_photos_from_camera_with_event,args=(start_event, step, port, camera_name,n_frames,cwd)))
            #take_frame_from_camera(port,filename)
            #time.sleep(4)
            #filename = f"camera_{n+1}_video.mp4"
        #executor.submit(capture_video_from_camera, port, filename)

        #take_photo_from_camera(port,f"img_{n}.png")
    for t in threads:
        t.start()
    time.sleep(2)
    start_event.set()

    #SOMETIMES IT TIMES OUT AND YOU LITERALLY JUST NEED TI PLUG AND UNPLUG IT AGAIN which is stupid ik