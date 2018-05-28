# coding: utf-8

#""" tennis-balls-detection-v5.py: Detect tennis ball, draw bounding box, display distance, update distance to deep stream server with timestamp"""
#___ Author___  =  "Zhangying (Mandy) He"
#___email___  = "mandyhe@csu.fullerton.edu"

import tensorflow as tf
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import time
from deepstream import get, post
from scipy.stats import norm
import os, sys
import urllib
import tarfile
import cv2
from utils import visualization_utils as vis_util
from io import StringIO
from utils import label_map_util
import threading

slim = tf.contrib.slim

# ## Prepare models
NUM_CLASSES = 90

# List of the strings that is used to add correct label for each box.
CWD_PATH = os.getcwd()
PATH_TO_LABELS = os.path.join(CWD_PATH,'object_detection', 'data', 'mscoco_label_map.pbtxt')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

MODELS_DIR='models'

## Video Capture & Record
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

filename = 1
while os.path.isfile("output/video_"+str(filename)+".mp4"):
    filename += 1

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
#out = cv2.VideoWriter("output/video_"+str(filename)+'.mp4', fourcc, 15.0, (1280, 720))
#out = cv2.VideoWriter("output/video_"+str(filename)+'.mp4', fourcc, 15.0, (1920, 1080))
out = cv2.VideoWriter("output/video_"+str(filename)+'.mp4', fourcc, 10.0, (640, 480),True)
cap.set(3,IMAGE_WIDTH)
cap.set(4,IMAGE_HEIGHT)

# Colors (one for each class)
cmap = ImageColor.colormap

COLOR_LIST = sorted([c for c in cmap.keys()])

def filter_boxes(min_score,boxes, scores, classes, categories):
    """Return boxes with a confidence >= `min_score`"""
    n = len(classes)
    idxs = []
    for i in range(n):
        if classes[i] in categories and scores[i] >= min_score:
        #if classes[i] in categories:
            idxs.append(i)
    
    filtered_boxes = boxes[idxs, ...]
    filtered_scores = scores[idxs, ...]
    filtered_classes = classes[idxs, ...]
    return filtered_boxes, filtered_scores, filtered_classes

def to_image_coords(boxes, height, width):
    """
    The original box coordinate output is normalized, i.e [0, 1].
    
    This converts it back to the original coordinate based on the image
    size.
    """
    box_coords = np.zeros_like(boxes)
    box_coords[:, 0] = boxes[:, 0] * height
    box_coords[:, 1] = boxes[:, 1] * width
    box_coords[:, 2] = boxes[:, 2] * height
    box_coords[:, 3] = boxes[:, 3] * width
    
    return box_coords

def draw_boxes(image, boxes, classes, thickness=4):
    """Draw bounding boxes on the image"""
    draw = ImageDraw.Draw(image)
    for i in range(len(boxes)):
        bot, left, top, right = boxes[i, ...]
        class_id = int(classes[i])
        color = COLOR_LIST[class_id]
        draw.line([(left, top), (left, bot), (right, bot), (right, top), (left, top)], width=thickness, fill=color)

def ilustrate_detection(image,boxes, classes,title):
    # The current box coordinates are normalized to a range between 0 and 1.
    # This converts the coordinates actual location on the image.
    # Each class with be represented by a differently colored box
    draw_boxes(image, box_coords, classes)
    image = cv2.imread(image)
    draw_boxes(image, boxes, classes)
    fig = plt.figure(figsize=(12, 8))
    fig.suptitle(title, fontsize=10)
    plt.imshow(image)

def bboxes_draw_on_img(img, scores, boxes, colors, thickness=2, show_text=True):
    """Drawing bounding boxes on an image, with additional text if wanted...
        """
    shape = img.shape
    for i in range(boxes.shape[0]):
        bbox = boxes[i]
        color = colors[i % len(colors)]
        # Draw bounding box...
        p1 = (int(bbox[0] * shape[0]), int(bbox[1] * shape[1]))
        p2 = (int(bbox[2] * shape[0]), int(bbox[3] * shape[1]))
        cv2.rectangle(img, p1[::-1], p2[::-1], color, thickness)
        # Draw text...
        if show_text:
            s1 = '%s: %s' % ('Tennis Ball', scores[i]) + 'detected distance: {} cm.' .format(dist)
            p1 = (p1[0]-5, p1[1])
            cv2.putText(img, s, p1[::-1], cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 1)

def plot_image(img, title='', figsize=(24, 9)):
    f, axes = plt.subplots(1, 1, figsize=figsize)
    f.tight_layout()
    axes.imshow(img)
    axes.set_title(title, fontsize=20)

# ## Model functions

def load_graph(graph_file):
    """Loads a frozen inference graph"""
    graph = tf.Graph()
    with graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(graph_file, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        # The input placeholder for the image.
        # `get_tensor_by_name` returns the Tensor with the associated name in the Graph.
        image_tensor = graph.get_tensor_by_name('image_tensor:0')

        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = graph.get_tensor_by_name('detection_boxes:0')

        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = graph.get_tensor_by_name('detection_scores:0')

        # The classification of the object (integer id).
        detection_classes = graph.get_tensor_by_name('detection_classes:0')
    return graph, image_tensor, detection_boxes,detection_scores,detection_classes


def detect(detection_graph,
           image_tensor, 
           detection_boxes,
           detection_scores,
           detection_classes,
           image_np,
           categories,
           runs=1):
  
    with tf.Session(graph=detection_graph) as sess:                
        # Actual detection.
        
        times = np.zeros(runs)
        for i in range(runs):
            t0 = time.time()
            (boxes, scores, classes) = sess.run([detection_boxes, detection_scores, detection_classes], 
                                                feed_dict={image_tensor: image_np})
            t1 = time.time()
            times[i] = (t1 - t0) * 1000

        # Remove unnecessary dimensions
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes)

        return boxes, scores, classes,time

# function to find the marker of the center point of the tennis ball bboxes
def find_marker(boxes):
    # find the center point of the detected box
    y1 = boxes[:,0]
    x1 = boxes[:,1]
    y2 = boxes[:,2]
    x2 = boxes[:,3]
    ymidPoint = ((y2-y1)/2)
    xmidPoint = ((x2-x1)/2)
    midPoint = ymidPoint,xmidPoint
    midPoint = np.concatenate((midPoint[0],midPoint[1]),axis = 0)
    return midPoint

#
def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

# ## Find the focal length using a known-distance tennis ball

# initialize the known distance from the camera to the object, which
# in this case is 20cm
KNOWN_DISTANCE = 20

# initialize the known object width, the diameter for a regular tennis ball
# is 6.8 cm, so the width of the detection box should be the same size
KNOWN_WIDTH = 6.8

# initialize the list of images that we'll be using
import glob
frozen_model_paths=[graph for graph in glob.iglob(MODELS_DIR+'/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb',recursive=False)]
#sim_image_paths= [graph for graph in glob.iglob('20cm.png', recursive=False)]
sim_image_paths= [graph for graph in glob.iglob('20cm_webcam.png', recursive=False)]
tennis_ball_class_id = 37
test_image=sim_image_paths[0]
confidence_cutoff = 0.01

# Detecting tennis balls with Mobilenet
mobilenet=frozen_model_paths[0]
detection_graph,image_tensor,detection_boxes,detection_scores,detection_classes = load_graph(mobilenet)
image = Image.open(test_image)
image_np = np.expand_dims(np.asarray(image, dtype=np.uint8), 0)
boxes,scores,classes,_ = detect(detection_graph,
                                image_tensor,
                                detection_boxes,
                                detection_scores,
                                detection_classes,
                                image_np,
                                tennis_ball_class_id)
boxes, scores, classes = filter_boxes(confidence_cutoff, boxes, scores, classes,[tennis_ball_class_id])

marker = find_marker(boxes)
focalLength = (marker[1] * KNOWN_DISTANCE) / KNOWN_WIDTH

# ## Detecting tennis balls with Mobilenet

mobilenet=frozen_model_paths[0]
detection_graph,image_tensor,detection_boxes,detection_scores,detection_classes = load_graph(mobilenet)
with tf.Session(graph=detection_graph) as sess:
    while True:
        t = time.time()
        ret, image_np = cap.read()
        image_np_expanded = np.expand_dims(image_np,axis=0)
        (boxes, scores, classes) = sess.run([detection_boxes, detection_scores, detection_classes],
                                            feed_dict={image_tensor: image_np_expanded})
        boxes,scores,classes,_ = detect(detection_graph,
                                      image_tensor,
                                      detection_boxes,
                                      detection_scores,
                                      detection_classes,
                                      image_np_expanded,
                                      tennis_ball_class_id)
        confidence_cutoff = 0.001

        # Filter boxes from other detected objects
        filtered_boxes, filtered_scores, filtered_classes = filter_boxes(confidence_cutoff, boxes, scores, classes,[tennis_ball_class_id])
        if filtered_boxes.shape[0] > 0:
            # find the distance of the tennis ball
            marker = find_marker(filtered_boxes)
            dist = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1])
            dist_around = np.around(dist)

            try:
                post({ "ball": dist_around, "time" : time.time() }, "objectDetection")
            except:
                print("deepstream is either not running, or something else.")
            vis_util.visualize_boxes_and_labels_on_image_array(
                                                               image_np,
                                                               filtered_boxes,
                                                               (filtered_classes).astype(np.int32),
                                                               filtered_scores,
                                                               category_index,
                                                               max_boxes_to_draw = 1,
                                                               min_score_thresh = 0.001,
                                                               use_normalized_coordinates=True,
                                                               line_thickness=8)

        # Visualization of the results of a detection.
            cv2.putText(image_np,"detected distance is {} cm." .format(dist_around),(10,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("tennis ball detection",image_np)
        out.write(image_np)
        print(time.time() - t)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
out.release()
cv2.destroyAllWindows()

