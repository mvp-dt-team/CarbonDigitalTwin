import cv2
from ultralytics import YOLO
from PIL import Image
import numpy as np
from matplotlib import cm
import pandas as pd

def loop_predict(video_path, model_path, gif_path, csv_path):

    # Load the YOLOv8 model
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    frames = []
    pandas_data = []
    count = 0

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            count += 1
            # Run YOLOv8 inference on the frame
            results = model(frame)
            pandas_data.append(results[0].speed)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            
            if count % 30 == 0:
                frames.append(annotated_frame)

            # Display the annotated frame
            # cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    im = Image.fromarray(np.uint8(frames[0]))
    frames_image = []
    for i in frames[1:]:
        frames_image.append(Image.fromarray(np.uint8(i)))
    im.save(gif_path, save_all=True, append_images=frames_image, optimize=True,
        duration=1, loop=True)

    df = pd.DataFrame(data=pandas_data)
    df.to_csv(csv_path)

if __name__ == '__main__':
    video_path1 = "test/WEB_light.mp4"
    model_path1 = "YOLO8l_best.pt"
    gif_path1 = "YOLO8l_result_light.gif"
    csv_path1 = "YOLO8l_result_light.csv"

    video_path2 = "test/WEB_dark.mp4"
    model_path2 = "YOLO8l_best.pt"
    gif_path2 = "YOLO8l_result_dark.gif"
    csv_path2 = "YOLO8l_result_dark.csv"

    loop_predict(video_path1, model_path1, gif_path1, csv_path1)
    loop_predict(video_path2, model_path2, gif_path2, csv_path2)