import subprocess

def take_photo():
    try:
        subprocess.run(["gphoto2", "--capture-image-and-download", "--filename", "photo.jpg"], check=True)
        print("Photo taken and saved as photo.jpg")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

take_photo()
