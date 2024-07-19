import pyrealsense2 as rs
import numpy as np
import cv2
import json
from datetime import datetime
import detect
import math

# Configure depth and color streams
photo_width = 1280
photo_height = 720
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Create an align object
align_to = rs.stream.color
align = rs.align(align_to)

save_photo_path = "flowers/"

# Create a JSON object to save depth data
def get_flowers_center_postions(flower_boxes,positons_map):
    positons = []
    for box in flower_boxes:
        U = math.floor(box[0] * photo_width)
        V = math.floor(box[1] * photo_height)
        positons.append(positons_map[V][U])
    return positons


def get_current_flowers_info():
    try:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            return

        # Get intrinsics
        intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

        # Initialize the JSON array with appropriate dimensions
        depth_data_json = [[{} for _ in range(intrinsics.width)] for _ in range(intrinsics.height)]
        # Save the depth data to the JSON object
        for y in range(intrinsics.height):
            for x in range(intrinsics.width):
                # Get the depth value in meters
                depth_value = depth_frame.get_distance(x, y)

                # Convert from pixel coordinates to camera coordinates
                point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth_value)

                # Save the coordinates in the JSON object
                depth_data_json[y][x] = {
                    "x": point[0],
                    "y": point[1],
                    "z": point[2]
                }
        # Convert color frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())
        filename = save_photo_path + datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"
        cv2.imwrite(filename, color_image)
        opt = detect.parse_opt(filename)
        boxes = detect.run(**vars(opt))
        return get_flowers_center_postions(boxes,depth_data_json)
    except:
        pass



