"""
Custom node to show keypoints and check posture
"""

from typing import Any, Dict, List, Tuple
import cv2
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

# setup global constants
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)       # opencv loads file in BGR format
YELLOW = (0, 255, 255)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
THRESHOLD = 0.5               # ignore keypoints below this threshold
KP_NOSE = 0                   # PoseNet's skeletal keypoints
KP_RIGHT_EAR = 4
KP_RIGHT_SHOULDER = 6         
KP_RIGHT_HIP = 12
KP_LEFT_EAR = 3
KP_LEFT_SHOULDER = 5        
KP_LEFT_HIP = 11


def map_bbox_to_image_coords(
   bbox: List[float], image_size: Tuple[int, int]
) -> List[int]:
   """First helper function to convert relative bounding box coordinates to
   absolute image coordinates.
   Bounding box coords ranges from 0 to 1
   where (0, 0) = image top-left, (1, 1) = image bottom-right.

   Args:
      bbox (List[float]): List of 4 floats x1, y1, x2, y2
      image_size (Tuple[int, int]): Width, Height of image

   Returns:
      List[int]: x1, y1, x2, y2 in integer image coords
   """
   width, height = image_size[0], image_size[1]
   x1, y1, x2, y2 = bbox
   x1 *= width
   x2 *= width
   y1 *= height
   y2 *= height
   return int(x1), int(y1), int(x2), int(y2)


def map_keypoint_to_image_coords(
   keypoint: List[float], image_size: Tuple[int, int]
) -> List[int]:
   """Second helper function to convert relative keypoint coordinates to
   absolute image coordinates.
   Keypoint coords ranges from 0 to 1
   where (0, 0) = image top-left, (1, 1) = image bottom-right.

   Args:
      bbox (List[float]): List of 2 floats x, y (relative)
      image_size (Tuple[int, int]): Width, Height of image

   Returns:
      List[int]: x, y in integer image coords
   """
   width, height = image_size[0], image_size[1]
   x, y = keypoint
   x *= width
   y *= height
   return int(x), int(y)


def draw_text(img, x, y, text_str: str, color_code):
   """Helper function to call opencv's drawing function,
   to improve code readability in node's run() method.
   """
   cv2.putText(
      img=img,
      text=text_str,
      org=(10*x, 18*y),
      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
      fontScale=0.6,
      color=color_code,
      thickness=2,
   )

class Node(AbstractNode):
   #Custom node to display keypoints and check posture

   def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
      super().__init__(config, node_path=__name__, **kwargs)
      # setup object working variables
      self.tick = 0
      self.tock = 0
      self.head = [0,0] #tilt upward, tilt downward
      self.neck = [0,0] #neck forward, neck backward
      self.back = [0,0] #lean forward, lean backward

   def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
      """This node draws keypoints and checks posture.

      Args:
            inputs (dict): Dictionary with keys
               "img", "bboxes", "bbox_scores", "keypoints", "keypoint_scores".

      Returns:
            outputs (dict): Empty dictionary.
      """

      # get required inputs from pipeline
      img = inputs["img"]
      bboxes = inputs["bboxes"]
      bbox_scores = inputs["bbox_scores"]
      keypoints = inputs["keypoints"]
      keypoint_scores = inputs["keypoint_scores"]

      img_size = (img.shape[1], img.shape[0])  # image width, height

      # get bounding box confidence score and draw it at the
      # left-bottom (x1, y2) corner of the bounding box (offset by 30 pixels)
      if len(bboxes) > 0 and len(bbox_scores) > 0:
         the_bbox = bboxes[0]             # image only has one person
         the_bbox_score = bbox_scores[0]  # only one set of scores

         x1, y1, x2, y2 = map_bbox_to_image_coords(the_bbox, img_size)
         score_str = f"BBox {the_bbox_score:0.2f}"
         cv2.putText(
            img=img,
            text=score_str,
            org=(x1, y2 - 30),            # offset by 30 pixels
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=WHITE,
            thickness=1,
         )

      # posture detection using a simple heuristic of tracking nose, ear, shoulder and hip relative position
      nose = None
      right_ear = None
      right_shoulder = None
      right_hip = None
      left_ear = None
      left_shoulder = None
      left_hip = None
      right_score = 0
      left_score = 0

      if len(keypoints) > 0 and len(keypoint_scores) > 0:
         the_keypoints = keypoints[0]  # image only has one person
         the_keypoint_scores = keypoint_scores[0]
            
         for i, keypoints in enumerate(the_keypoints):
            keypoint_score = the_keypoint_scores[i]

            if keypoint_score >= THRESHOLD:
               x, y = map_keypoint_to_image_coords(keypoints.tolist(), img_size)
               x_y_str = f"({x}, {y})"

               if i == KP_NOSE:
                  nose = keypoints
                  the_color = YELLOW
               elif i == KP_RIGHT_EAR:
                  right_ear = keypoints
                  right_score += keypoint_score
                  the_color = YELLOW
               elif i == KP_RIGHT_SHOULDER:
                  right_shoulder = keypoints
                  right_score += keypoint_score
                  the_color = YELLOW
               elif i == KP_RIGHT_HIP:
                  right_hip = keypoints
                  right_score += keypoint_score
                  the_color = YELLOW
               elif i == KP_LEFT_EAR:
                  left_ear = keypoints
                  left_score += keypoint_score
                  the_color = YELLOW
               elif i == KP_LEFT_SHOULDER:
                  left_shoulder = keypoints
                  left_score += keypoint_score
                  the_color = YELLOW
               elif i == KP_LEFT_HIP:
                  left_hip = keypoints
                  left_score += keypoint_score
                  the_color = YELLOW
               else:                   # generic keypoint
                  the_color = WHITE

               draw_text(img, x, y, x_y_str, the_color)

      right = 0
      left = 0
      watching = "NA"
      for i in [right_ear, right_shoulder, right_hip]:
         if i is not None:
            right += 1
      for i in [left_ear, left_shoulder, left_hip]:
         if i is not None:
            left += 1

      if right > left:
         ear = right_ear
         shoulder = right_shoulder
         hip = right_hip
         watching = "right"
      elif left > right:
         ear = left_ear
         shoulder = left_shoulder
         hip = left_hip
         watching = "left"
      else:
         if right_score >= left_score:
            ear = right_ear
            shoulder = right_shoulder
            hip = right_hip
            watching = "right"
         else:
            ear = left_ear
            shoulder = left_shoulder
            hip = left_hip
            watching = "left"

      unit = None
      unit_str = "NA"
      nose_ear = None
      ear_shoulder = None
      shoulder_hip = None
      nose_ear_dist = None
      ear_shoulder_dist = None
      shoulder_hip_dist = None
      errored = False
      side = None
      opp = None

      if nose is None:
         draw_text(img, 1, 13, "Nose not found!", RED)
         errored = True
      if ear is None:
         draw_text(img, 1, 14, "Ear not found!", RED)
         errored = True
      if shoulder is None:
         draw_text(img, 1, 15, "Shoulder not found!", RED)
         errored = True
      if hip is None:
         draw_text(img, 1, 16, "Hip not found!", RED)
         errored = True

      if shoulder is not None and ear is not None:
         unit = ((ear[0]-shoulder[0])**2+(shoulder[1]-ear[1])**2)**0.5/10

         if left_shoulder is not None and right_shoulder is not None and hip is not None:
            torso_h = ((left_shoulder[0]-right_shoulder[0])**2+(left_shoulder[1]-right_shoulder[1])**2)**0.5
            if watching == "right":
               torso_v = ((right_shoulder[0]-right_hip[0])**2+(right_shoulder[1]-right_hip[1])**2)**0.5
            else:
               torso_v = ((left_shoulder[0]-left_hip[0])**2+(left_shoulder[1]-left_hip[1])**2)**0.5
            if torso_h >= torso_v/4:
               draw_text(img, 1, 12, "Camera angle incorrect!", RED)
               errored = True

         es = [[1.5, -1], [1, -1.5]]
         sh = [[2, -3], [3, -2]]
         ne = [[1, -2], [1, -2]]

         str_es = ["Bend neck backward!", "Bend neck forward!"]
         str_sh = ["Sit backward!", "Sit forward!"]
         str_ne = ["Tilt head down!", "Tilt head up!"]

         if watching == "left":
            side, opp = 1, 0
         else:
            side, opp = 0, 1

         unit_str = f"{round(unit, 3)}"

         ear_shoulder_dist = round(ear[0]-shoulder[0], 3)
         if ear_shoulder_dist > es[side][0]*unit:
            ear_shoulder = str_es[side]
            if errored == False:
               self.neck[0] += 1
         elif ear_shoulder_dist < es[side][1]*unit:
            ear_shoulder = str_es[opp]
            if errored == False:
               self.neck[1] += 1
         else:
            ear_shoulder = "Good"

         if hip is not None:
            shoulder_hip_dist = round(shoulder[0]-hip[0], 3)
            if shoulder_hip_dist > sh[side][0]*unit:
               shoulder_hip = str_sh[side]
               if errored == False:
                  self.back[0] += 1
            elif shoulder_hip_dist < sh[side][1]*unit:
               shoulder_hip = str_sh[opp]
               if errored == False:
                  self.back[1] += 1
            else:
               shoulder_hip = "Good"

         if nose is not None:
            nose_ear_dist = round(-(nose[1]-ear[1]), 3)
            if nose_ear_dist > ne[side][0]*unit:
               nose_ear = str_ne[0]
               if errored == False:
                  self.head[0] += 1
            elif nose_ear_dist < ne[side][1]*unit:
               nose_ear = str_ne[1]
               if errored == False:
                  self.head[1] += 1
            else:
               nose_ear = "Good"

      self.tick += 1
      if errored == False:
         self.tock += 1

      draw_text(img, 1, 1, f"Tick: {self.tick} Tock: {self.tock}", BLACK)
      draw_text(img, 20, 1, unit_str, YELLOW)
      draw_text(img, 1, 3, f"Nose-Ear {nose_ear}", BLACK)
      #draw_text(img, 1, 2, f"{nose_ear_dist}", YELLOW)
      draw_text(img, 1, 4, f"Too High: {self.head[0]} Too Low: {self.head[1]}", BLACK)
      draw_text(img, 1, 6, f"Ear-Shoulder {ear_shoulder}", BLACK)
      #draw_text(img, 1, 5, f"{ear_shoulder_dist}", YELLOW)
      draw_text(img, 1, 7, f"Too Forward: {self.neck[0]} Too Backward: {self.neck[1]}", BLACK)
      draw_text(img, 1, 9, f"Shoulder-Hip {shoulder_hip}", BLACK)
      #draw_text(img, 1, 8, f"{shoulder_hip_dist}", YELLOW)
      draw_text(img, 1, 10, f"Too Forward: {self.back[0]} Too Backward: {self.back[1]}", BLACK)
      draw_text(img, 1, 11, f"Monitoring side: {watching}", BLACK)

      return {"Tick": self.tick,
      "Tock": self.tock,
      "Head Angle High": self.head[0],
      "Head Angle Low": self.head[1],
      "Neck Angle Forward": self.neck[0],
      "Neck Angle Backward": self.neck[1],
      "Back Angle Forward": self.back[0],
      "Back Angle Backward": self.back[1]}