import subprocess
import time
import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import threading
import csv
import numpy as np

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

def clear_memory(ports):
    for port in ports:
        try:
            subprocess.run(["gphoto2", "--port",port,"--delete-all-files"],check=True)
            print(f"cleaned camera {port}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred with {port}: {e}")

def default_configs(ports,file_path="config_list.csv"):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        config=[row for row in reader]
    for port in ports:
        for [prop,value] in config:
            try:
                subprocess.run(["gphoto2","--port", port, "--set-config", f"{prop}={value}"],check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred with {port}: {e}")


from concurrent.futures import ThreadPoolExecutor

def take_photo_from_camera(port, filename):
    try:
        subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", filename], check=True)
        print(f"Photo taken from {port} and saved as {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred with {port}: {e}")

def reset_all(ports):
    for port in ports:
        try:
            #subprocess.run(["gphoto2", "--port", port, "--reset"], check=True)
            print(f"reset {port} ")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred with {port}: {e}")


def photos_from_camera_time_list(port,camera_name,time_list,cwd):
    i=0
    actual_times=[]
    start=time.time()
    while i<len(time_list):
        while time.time() < time_list[i]:
            pass
        subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download","--filename" ,f"img_{i}.jpg","--force-overwrite"],cwd=cwd)
        i+=1
        later=time.time()
        print(f"image {i} for {camera_name} saved at {later}")
        actual_times.append([later-start])
        start=later
    print(f"{camera_name}, std dev={np.std(actual_times)} mean {np.mean(actual_times)}")

def take_multiple_photos_from_camera_with_event(start_event,step,port,camera_name,n_frames,cwd):
    #print("called fucntion with  ",camera_name)
    files_in_dir = os.listdir()

# Check if any file contains the substring
    file_exists = any(camera_name in filename for filename in files_in_dir)
    if file_exists:
        return
    timestep="2ms"
    start_event.wait()
    start=time.time()
    print(camera_name," starting at ",start)
    #command=["gphoto2", "--port", port, "--capture-image", "--filename", camera_name+"_image-%03n.jpg","--force-overwrite" , f"--frames={n_frames}","--interval=2"]
    #command.append(["--debug" ,f"--debug-logfile=gphoto-debug-{camera_name}.log"])
    subprocess.run(["gphoto2", "--port", port, "--capture-image-and-download", "--filename", camera_name+"_image-%03n.jpg","--force-overwrite" , f"--frames={n_frames}",f"--interval={timestep}","--debug" ,f"--debug-logfile=gphoto-debug-{camera_name}.log",f"--wait-event={timestep}"],cwd=cwd)
    later=time.time()
    print(f"Frames taken from {port} and saved as {camera_name} at {later}")

    #subprocess.run(["gphoto2","--port", port, "--get-all-files"],check=True,cwd=cwd)

#def capture_video(port)

def warmup(ports):
    for port in ports:
        start=time.time()
        subprocess.run(["gphoto2", "--port", port, "--capture-image"])
        print(f"elpased {time.time()-start} secponds")

def thread_for_each_camera(start_event,time_list,ports):
    duration=15
    for n,port in enumerate(ports):
        cwd=f"imgdir_{n}"
        os.makedirs(cwd,exist_ok=True)
        n_frames=10
        camera_name= f"camera_{n}" #f"img_{n}_{k}.jpg"
        #executor.submit(take_multiple_photos_from_camera_with_event, start_event, step, port, camera_name,n_frames)
        threads.append(threading.Thread(target=take_multiple_photos_from_camera_with_event,args=(start_event, step, port, camera_name,n_frames,cwd)))
        #threads.append(threading.Thread(target=photos_from_camera_time_list,args=(port,camera_name,time_list,cwd)))
        #threads.append(threading.Thread(target=capture_video,args=(port,duration,cwd,camera_name,start_event)))
    for t in threads:
        t.start()
    time.sleep(10)
    start_event.set()

def capture_video(port,duration,cwd,camera_name,start_event):
    start_event.wait()
    start=time.time()
    print(camera_name," starting at ",start)
    subprocess.run(["gphoto2", "--port", port,"--capture-movie",str(duration)+"s"],cwd=cwd)
    end=time.time()
    print(f"{camera_name} video ended at {end} elapsed {end-start}")
    subprocess.run(["gphoto2","--port", port, "--get-all-files"],cwd=cwd)


if __name__=="__main__":

    #subprocess.run(["gphoto2", "--reset"])
    start_event = threading.Event()
    step=0.5
    ports=get_camera_ports()
    print(ports)
    reset_all(ports)
    warmup(ports)
    clear_memory(ports)
    #default_configs(ports)
    #with ThreadPoolExecutor() as executor:
    threads=[]
    start_time=time.time()
    time_list=[start_time+10+ x/2 for x in range(10)]
    print(time_list)
    thread_for_each_camera(start_event,time_list,ports)
            #take_frame_from_camera(port,filename)
            #time.sleep(4)
            #filename = f"camera_{n+1}_video.mp4"
        #executor.submit(capture_video_from_camera, port, filename)

        #take_photo_from_camera(port,f"img_{n}.png")
    

    #SOMETIMES IT TIMES OUT AND YOU LITERALLY JUST NEED TI PLUG AND UNPLUG IT AGAIN which is stupid ik