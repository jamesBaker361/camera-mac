import imageio
import os

# Open MJPEG video file
video_path = '/Users/jbaker15/Desktop/camera/imgdir_1/movie.mjpg'
reader = imageio.get_reader(video_path)

# Create an output folder to save frames
output_folder = 'extracted_frames'
os.makedirs(output_folder, exist_ok=True)

frame_count = 0

# Loop through the video frames
for frame in reader:
    frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
    imageio.imwrite(frame_filename, frame)
    frame_count += 1

print(f'Extracted {frame_count} frames.')
