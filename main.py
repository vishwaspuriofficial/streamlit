# import streamlit as st
# import cv2
# import os
# from streamlit_webrtc import VideoProcessorBase, webrtc_streamer
#
# noseCascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")
# mouthCascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
# class VideoProcessor(VideoProcessorBase):
#     def __init__(self):
#         self.i = 0
#
#     def transform(self, frame):
#     # Method 2: Write on Camera
#
#
#     # try:
#     #     try:
#     #         try:
#     #             cap = cv2.VideoCapture(0)
#     #         except:
#     #             cap = cv2.VideoCapture(1)
#     #     except:
#     #         cap = cv2.VideoCapture(2)
#     # except:
#     #     "Camera couldn't be turned on!"
#     #
#     #
#     # while True:
#     #
#     #     # Capture frame-by-frame
#     #     ret, frame = cap.read()
#     #     cameraOn = 1
#         frame = frame.to_ndarray(format="bgr24")
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#         nose = noseCascade.detectMultiScale(gray, 1.3, 5)
#         mouth = mouthCascade.detectMultiScale(gray, 1.3, 5)
#
#         i = self.i + 1
#         if len(nose) != 0 and len(mouth) != 0:
#             cv2.putText(frame, "No Mask!", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
#             return frame
#         # windowName = "Mask Detector"
#         # cv2.imshow(windowName, frame)
#         # cv2.setWindowProperty(windowName, cv2.WND_PROP_TOPMOST, 1)
#
#         # if cv2.waitKey(1) & 0xFF == ord('c'):
#         #     break
#
#     # When everything is done, release the capture
#     # cap.release()
#     # cv2.destroyAllWindows()
# #
# # # detectMask()
# #
# # cameraOn = 0
# #
# startCamera = st.button("Start Mask Detection", key="1")
# stopCamera = st.button("Stop Mask Detection", key="2")
# #
# # if startCamera:
# #     st.success('Mask Detector turning on!')
# #     #cv2.destroyAllWindows()
# #     detectMask()
# # if stopCamera:
# #     if cameraOn:
# #         cv2.destroyAllWindows()
# #
# # while cameraOn==0:
# #     pass
# # while cameraOn:
# #     pass
#
# if startCamera:
#     st.success("Turning on!")
#     webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
#
# if stopCamera:
#     cv2.destroyAllWindows()
import streamlit as st
import cv2
from streamlit_webrtc import (
    AudioProcessorBase,
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import av

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
def model():
    class OpenCVVideoProcessor(VideoProcessorBase):
        type: Literal["noop", "cartoon", "edges", "rotate"]

        def __init__(self) -> None:
            self.type = "noop"

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            if self.type == "noop":
                pass
            elif self.type == "cartoon":
                # prepare color
                img_color = cv2.pyrDown(cv2.pyrDown(img))
                for _ in range(6):
                    img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
                img_color = cv2.pyrUp(cv2.pyrUp(img_color))

                # prepare edges
                img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img_edges = cv2.adaptiveThreshold(
                    cv2.medianBlur(img_edges, 7),
                    255,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    9,
                    2,
                )
                img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

                # combine color and edges
                img = cv2.bitwise_and(img_color, img_edges)
            elif self.type == "edges":
                # perform edge detection
                img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
            elif self.type == "rotate":
                # rotate image
                rows, cols, _ = img.shape
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
                img = cv2.warpAffine(img, M, (cols, rows))

            return av.VideoFrame.from_ndarray(img, format="bgr24")


    webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=OpenCVVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.type = st.radio(
            "Select transform type", ("noop", "cartoon", "edges", "rotate")
        )

model()
