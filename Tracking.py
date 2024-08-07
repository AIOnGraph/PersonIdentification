
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
import av
from sample_utils import get_ice_servers
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, WebRtcMode
from utils import recognize, build_dataset
# from Tracking import VideoProcessor1
# Path: code\app.py
class VideoProcessor1(VideoProcessorBase):
    def __init__(self,tolerance):
        self.tolerance = tolerance 
        print(tolerance) # Example tolerance value

    def recv(self, frame):
        print(frame)
        img = frame.to_ndarray(format="bgr24")
        img, name, id = recognize(img, self.tolerance)
        # st.session_state['name'] = name
        # st.session_state['id'] = id
        # st.session_state['frame'] = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Initialize session state
# if 'name' not in st.session_state:
#     st.session_state['name'] = 'Unknown'
# if 'id' not in st.session_state:
#     st.session_state['id'] = 'Unknown'
# if 'frame' not in st.session_state:
#     st.session_state['frame'] = None

st.set_page_config(layout="wide")
#Config
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']



st.sidebar.title("Settings")



#Create a menu bar
menu = ["Picture","Webcam"]
choice = st.sidebar.selectbox("Input type",menu)
#Put slide to adjust tolerance
TOLERANCE = st.sidebar.slider("Tolerance",0.0,1.0,0.5,0.01)
st.sidebar.info("Tolerance is the threshold for face recognition. The lower the tolerance, the more strict the face recognition. The higher the tolerance, the more loose the face recognition.")
# def recv(frame):
#     img = frame.to_ndarray(format="bgr24")
#     img, name, id = recognize(img, TOLERANCE)
#     # st.session_state['name'] = name
#     # st.session_state['id'] = id
#     # st.session_state['frame'] = img
#     return av.VideoFrame.from_ndarray(img, format="bgr24")
#Infomation section 
st.sidebar.title("Information")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
name_container.info('Name: Unnknown')
id_container.success('ID: Unknown')
if choice == "Picture":
    st.title("Face Recognition App")
    st.write(PICTURE_PROMPT)
    uploaded_images = st.file_uploader("Upload",type=['jpg','png','jpeg'],accept_multiple_files=True)
    if len(uploaded_images) != 0:
        #Read uploaded image with face_recognition
        for image in uploaded_images:
            image = frg.load_image_file(image)
            # print(image)
            image, name, id = recognize(image,TOLERANCE) 
            name_container.info(f"Name: {name}")
            id_container.success(f"ID: {id}")
            st.image(image)
    else: 
        st.info("Please upload an image")
    
elif choice == "Webcam":
    st.title("Face Recognition App")
    st.write(WEBCAM_PROMPT)
    #Camera Settings
    # cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])
    # rtc_configuration = {"iceServers": [{"urls": "turn:relay1.expressturn.com:3478"}]}
    rtc_configuration={
        "iceServers": get_ice_servers()
    },
    webrtc_ctx = webrtc_streamer(
                key="example",
                # video_frame_callback=VideoProcessor1(TOLERANCE),
                video_processor_factory=lambda: VideoProcessor1(TOLERANCE),
                mode=WebRtcMode.SENDRECV,
                media_stream_constraints={
                        "video": True,
                        "audio": False,
                    },
                rtc_configuration=rtc_configuration,
        #         rtc_configuration={
        #     "iceServers": get_ice_servers(),
        #     "iceTransportPolicy": "relay",
        # },
                async_processing=True,
                
                # video_frame_callback=processor.recv
            )
    # while True:
    #     ret, frame = cam.read()
    #     if not ret:
    #         st.error("Failed to capture frame from camera")
    #         st.info("Please turn off the other app that is using the camera and restart app")
    #         st.stop()
    # image, name, id = recognize(frame,TOLERANCE)
    # while webrtc_ctx.state.playing:
    #     if st.session_state['frame'] is not None:
    #         frame_rgb = cv2.cvtColor(st.session_state['frame'], cv2.COLOR_BGR2RGB)
    #         FRAME_WINDOW.image(frame_rgb)
    #         name_container.info(f"Name: {st.session_state['name']}")
    #         id_container.success(f"ID: {st.session_state['id']}")
    
    
    # image = cv2.cvtColor(st.session_state['frame'], cv2.COLOR_BGR2RGB)
        # #Display name and ID of the person
        
    # name_container.info(f"Name: {name}")
    # id_container.success(f"ID: {id}")
    # FRAME_WINDOW.image(image)

with st.sidebar.form(key='my_form'):
    st.title("Developer Section")
    submit_button = st.form_submit_button(label='REBUILD DATASET')
    if submit_button:
        with st.spinner("Rebuilding dataset..."):
            build_dataset()
        st.success("Dataset has been reset")