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
THRESHOLD = 0.5               # ignore keypoints below this threshold
KP_NOSE = 0                   # PoseNet's skeletal keypoints
KP_RIGHT_EAR = 4
KP_RIGHT_SHOULDER = 6         
KP_RIGHT_HIP = 12


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
      org=(x, y),
      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
      fontScale=0.3,
      color=color_code,
      thickness=1,
   )


class Node(AbstractNode):
   #Custom node to display keypoints and check posture

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
            fontScale=0.3,
            color=WHITE,
            thickness=1,
         )

      # neck posture detection using a simple heuristic of tracking the
      # right ear position relative to right shoulder
      the_keypoints = None
      nose = None
      right_ear = None
      right_shoulder = None
      right_hip = None

      if len(keypoints) > 0 and len(keypoint_scores) > 0:
         the_keypoints = keypoints[0]  # image only has one person
         the_keypoint_scores = keypoint_scores[0]  # only one set of scores
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
                  the_color = YELLOW
               elif i == KP_RIGHT_SHOULDER:
                  right_shoulder = keypoints
                  the_color = YELLOW
               elif i == KP_RIGHT_HIP:
                  right_hip = keypoints
                  the_color = YELLOW
               else:                   # generic keypoint
                  the_color = WHITE

               draw_text(img, x, y, x_y_str, the_color)

      unit = None
      unit_str = "NA"
      nose_ear = None
      ear_shoulder = None
      shoulder_hip = None

      if nose is None:
         draw_text(img, 8, 2, "Nose not found!", RED)
      if right_ear is None:
         draw_text(img, 8, 10, "Ear not found!", RED)
      if right_shoulder is None:
         draw_text(img, 8, 18, "Shoulder not found!", RED)
      if right_hip is None:
         draw_text(img, 8, 26, "Hip not found!", RED)

      if right_shoulder is not None and right_hip is not None:
         unit = ((right_ear[0]-right_shoulder[0])**2+(right_shoulder[1]-right_ear[1])**2)**0.5/10
         unit_str = f"{unit}"
         if right_shoulder[0]-right_hip[0] > -6*unit and right_shoulder[0]-right_hip[0] < 1*unit:
            shoulder_hip = "Good"
         else:
            shoulder_hip = "Bad"

         if nose is not None and right_ear is not None:
            if abs(nose[1]-right_ear[1]) < 2*unit:
               nose_ear = "Good"
            else:
               nose_ear = "Bad"

         if right_ear is not None and right_shoulder is not None:
            if right_ear[0]-right_shoulder[0] > -1*unit and right_ear[0]-right_shoulder[0] < 3*unit:
               ear_shoulder = "Good"
            else:
               ear_shoulder = "Bad"

      pos_str = f"Nose-Ear {nose_ear} / Ear-Shoulder {ear_shoulder} / Shoulder-Hip {shoulder_hip}"
      draw_text(img, 8, 44, unit_str, YELLOW)
      draw_text(img, 8, 36, pos_str, YELLOW)

      return {}