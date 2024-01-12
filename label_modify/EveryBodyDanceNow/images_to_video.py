import cv2
import os

# Directory containing your images
image_folder = 'results/new_local/test_latest/images'

# Output video file
video_name = 'new_local_video.mp4'

# Get the list of image files
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

# Sort the images based on their names (assuming the names are in numerical order)
images.sort(key=lambda x: x.split('.')[0])

# Determine the width and height from the first image
img = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = img.shape

# Create a VideoWriter object
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

# Add images to the video
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))
    print(f'wrote {image} into video')

# Release the VideoWriter object
video.release()
