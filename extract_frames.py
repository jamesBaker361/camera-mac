import cv2
import os

# Open MJPEG video file
video_path = '/Users/jbaker15/Desktop/camera/imgdir_1/movie.mjpg'
cap = cv2.VideoCapture(video_path)

# Create an output folder to save frames
output_folder = 'extracted_frames'
os.makedirs(output_folder, exist_ok=True)

frame_count = 0

# Loop through the video frames
while True:
    ret, frame = cap.read()
    if not ret:
        break  # No more frames to read

    # Save frame as an image
    frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_filename, frame)

    frame_count += 1

# Release the video capture object
cap.release()
print(f'Extracted {frame_count} frames.')
