
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
import av
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, WebRtcMode
from streamlit_webrtc import webrtc_streamer
from sample_utils import get_ice_servers,perform_cleanup
from recognization_utils import recognize
import os 
cfg = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
PKL_PATH = cfg['PATH']['PKL_PATH']







class VideoProcessor1(VideoProcessorBase):
    def __init__(self, tolerance):
        self.tolerance = tolerance 

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img, name, id = recognize(img, self.tolerance)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.set_page_config(layout="wide")
# st.write(st.session_state)
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

if not st.session_state.initialized:
    perform_cleanup(PKL_PATH)
    st.session_state.initialized = True

PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']



st.sidebar.title("Settings")



#Create a menu bar
menu = ["Picture","Webcam"]
choice = st.sidebar.selectbox("Input type",menu)
#Put slide to adjust tolerance
TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.5,0.01)
st.sidebar.info("Tolerance is the threshold for Person recognition. The lower the tolerance, the more strict the Person recognition. The higher the tolerance, the more loose the Person recognition.")

#Infomation section 
st.sidebar.title("Information")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
name_container.info('Name: Unknown')
id_container.success('ID: Unknown')
if choice == "Picture":
    st.title("Person Recognition App")
    st.write(PICTURE_PROMPT)
    uploaded_images = st.file_uploader("Upload",type=['jpg','png','jpeg'],accept_multiple_files=True)
    if len(uploaded_images) != 0:
       
        for image in uploaded_images:
            image = frg.load_image_file(image)
            image, name, id = recognize(image,TOLERANCE) 
            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            st.image(image)
    else: 
        st.info("Please upload an image")
    
elif choice == "Webcam":
    st.title("Person Recognition App")
    st.write(WEBCAM_PROMPT)

    FRAME_WINDOW = st.image([])
    webrtc_streamer(key="sample",mode=WebRtcMode.SENDRECV,rtc_configuration={
            "iceServers": get_ice_servers(),
            "iceTransportPolicy": "relay",
        },
        media_stream_constraints={
                        "video": True,
                        "audio": False,
                    },
        video_processor_factory=lambda: VideoProcessor1(TOLERANCE),
        async_processing=True
        )
    

    
    
    





 