import cv2
import random
import os
import numpy as np
import sys  # Import sys to use sys.exit()

# Directory containing all series
mediaDirectory = "Media"

# Get the list of all series directories
seriesListDirectories = os.listdir(mediaDirectory)
print("Directories in '", mediaDirectory, "' :", seriesListDirectories)

# Set the active series to a randomly chosen one
activeSeries = random.choice(seriesListDirectories)
print("Active series: ", activeSeries)

# Get the path to the active series directory
activeSeriesPath = os.path.join(mediaDirectory, activeSeries)

# List all files in the active series directory
episodeList = os.listdir(activeSeriesPath)

# Filter out directories if needed, to only select files
episodeList = [file for file in episodeList if os.path.isfile(os.path.join(activeSeriesPath, file))]

# Sort the list
episodeList.sort()

# Check if there are episodes in the directory
if episodeList:
    # Start with the first episode
    activeEpisodeIndex = 0
    activeEpisode = episodeList[activeEpisodeIndex]
    print("Active episode: ", activeEpisode)
else:
    print("No episodes found in the selected series.")
    exit()  # Exit if no episodes are found


def play_episode(episode_path):
    # Load the video file
    print("Playing:", episode_path)
    cap = cv2.VideoCapture(episode_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Get screen width and height
    screen_width = 1920  # Set the width of your screen here (e.g., 1920)
    screen_height = 1080  # Set the height of your screen here (e.g., 1080)

    # Loop to read and display video frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            # If no more frames, break and move to the next episode
            break

        # Get the original frame size
        frame_height, frame_width = frame.shape[:2]

        # Calculate the aspect ratio of the video
        frame_aspect = frame_width / frame_height
        screen_aspect = screen_width / screen_height

        if frame_aspect > screen_aspect:
            # Video is wider than screen, add black bars on top and bottom
            new_width = screen_width
            new_height = int(screen_width / frame_aspect)
            if new_height > screen_height:
                new_height = screen_height
                new_width = int(screen_height * frame_aspect)
            resized_frame = cv2.resize(frame, (new_width, new_height))
            # Add black bars on top and bottom
            top_bottom_padding = (screen_height - new_height) // 2
            black_background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
            black_background[top_bottom_padding:top_bottom_padding + new_height, (screen_width - new_width) // 2:(screen_width - new_width) // 2 + new_width] = resized_frame
        else:
            # Video is taller than screen, add black bars on the sides
            new_height = screen_height
            new_width = int(screen_height * frame_aspect)
            if new_width > screen_width:
                new_width = screen_width
                new_height = int(screen_width / frame_aspect)
            resized_frame = cv2.resize(frame, (new_width, new_height))
            # Add black bars on left and right
            left_right_padding = (screen_width - new_width) // 2
            black_background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
            black_background[(screen_height - new_height) // 2:(screen_height - new_height) // 2 + new_height, left_right_padding:left_right_padding + new_width] = resized_frame

        # Create a window named 'Video'
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

        # Make the window fullscreen
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Display the frame with black bars
        cv2.imshow('Video', black_background)

        # Break the loop on 'q' key press
        if cv2.waitKey(25) & 0xFF == ord('q'):
            exit()

    # Release the video capture object
    cap.release()


def main():
    global activeEpisodeIndex
    try:
        while True:
            # Construct the path for the current episode
            video_path = os.path.join(mediaDirectory, activeSeries, episodeList[activeEpisodeIndex])

            # Play the current episode
            play_episode(video_path)

            # Move to the next episode
            activeEpisodeIndex += 1

            # If we reach the end of the episode list, loop back to the first episode
            if activeEpisodeIndex >= len(episodeList):
                activeEpisodeIndex = 0
    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
        cv2.destroyAllWindows()
        sys.exit()  # Force exit on Ctrl+C


if __name__ == "__main__":
    main()

# Close all OpenCV windows at the end
cv2.destroyAllWindows()
