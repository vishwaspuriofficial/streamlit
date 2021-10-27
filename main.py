

import streamlit as st
import cv2
import mediapipe as mp
import random
import os

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

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
st.header("Hand Photo Capture")
st.write("Press start to turn on Camera and If you want to click a picture, show the camera a peace sign ✌")
st.write("If camera dosen't turn on, click the select device button and change the camera input!")

def handPhotoCapture():
    class OpenCVVideoProcessor(VideoProcessorBase):
        type: Literal["hand"]



        def __init__(self) -> None:
            self.type = "hand"


        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            def filename():
                i = random.randint(1, 100000000000000)
                check = str(i) + ".jpg"
                if check in os.listdir():
                    filename()
                else:
                    return i

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            lmList = []
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    lmList.append(handLms)
                if len(lmList) != 0:
                    if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][
                        2] and lmList[20][2] > lmList[18][2]:
                        # Check if index and middle finder are open
                        # print("Finger Open")
                        i = filename()
                        img_name = "{}.jpg".format(i)
                        cv2.imwrite(img_name, img)
                        print("{} written!".format(img_name))
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
        webrtc_ctx.video_processor.type = "hand"

if __name__ == "__main__":
    handPhotoCapture()


