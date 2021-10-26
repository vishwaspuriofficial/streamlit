import streamlit as st

cameraOn = 0

startCamera = st.button("Start Mask Detection", key="1")
stopCamera = st.button("Stop Mask Detection", key="2")

if startCamera:
    while cameraOn==0:
        st.write("hello")
        st.spinner('Mask Detector Activating')

    st.success('Mask Detector Ready!')
    # cv2.destroyAllWindows()



