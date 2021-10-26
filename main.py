import streamlit as st
import cv2
import os

cameraOn = 0

startCamera = st.button("Start Mask Detection", key="1")
stopCamera = st.button("Stop Mask Detection", key="2")

if startCamera:
    while cameraOn ==0:
        st.spinner('Mask Detector Activating')

    st.success('Mask Detector Ready!')
    # cv2.destroyAllWindows()

    # detectMask()
if stopCamera:
    if cameraOn:
        cv2.destroyAllWindows()

while cameraOn==0:
    pass
while cameraOn:
    pass


