import streamlit as st
import cv2
import os
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

noseCascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
mouthCascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.i = 0

    def transform(self, frame):
    # Method 2: Write on Camera


    # try:
    #     try:
    #         try:
    #             cap = cv2.VideoCapture(0)
    #         except:
    #             cap = cv2.VideoCapture(1)
    #     except:
    #         cap = cv2.VideoCapture(2)
    # except:
    #     "Camera couldn't be turned on!"
    #
    #
    # while True:
    #
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #     cameraOn = 1
        frame = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        nose = noseCascade.detectMultiScale(gray, 1.3, 5)
        mouth = mouthCascade.detectMultiScale(gray, 1.3, 5)

        i = self.i + 1
        if len(nose) != 0 and len(mouth) != 0:
            cv2.putText(frame, "No Mask!", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            return frame
        # windowName = "Mask Detector"
        # cv2.imshow(windowName, frame)
        # cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)

        # if cv2.waitKey(1) & 0xFF == ord('c'):
        #     break

    # When everything is done, release the capture
    # cap.release()
    # cv2.destroyAllWindows()
#
# # detectMask()
#
# cameraOn = 0
#
startCamera = st.button("Start Mask Detection", key="1")
stopCamera = st.button("Stop Mask Detection", key="2")
#
# if startCamera:
#     st.success('Mask Detector turning on!')
#     #cv2.destroyAllWindows()
#     detectMask()
# if stopCamera:
#     if cameraOn:
#         cv2.destroyAllWindows()
#
# while cameraOn==0:
#     pass
# while cameraOn:
#     pass

if startCamera:
    st.success("Turning on!")
    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

if stopCamera:
    cv2.destroyAllWindows()