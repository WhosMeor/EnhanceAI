import streamlit as st
import cv2
import os
import numpy as np
from account import get_user_session_state
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer
from gfpgan import GFPGANer
from streamlit_image_comparison import image_comparison

# Function to load the model
def load_model(model_name, model_path, denoise_strength, tile, tile_pad, pre_pad, fp32, gpu_id):
    st.write("Upsampling...")
    if model_name == 'General':
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
    elif model_name == 'Anime':
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth']

    # Determine model paths
    if model_path is not None:
        model_path = model_path
    else:
        model_path = os.path.join('weights', model_name + '.pth')
        if not os.path.isfile(model_path):
            for url in file_url:
                # Model_path will be updated
                model_path = load_file_from_url(
                    url=url, model_dir=os.path.join(os.getcwd(), 'weights'), progress=True, file_name=model_name + '.pth')

    # Restorer
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=denoise_strength,
        model=model,
        tile=tile,
        tile_pad=tile_pad,
        pre_pad=pre_pad,
        half=fp32,
        gpu_id=gpu_id)
    return upsampler

# Function to download model weights if not present
def ensure_model_weights(model_name):
    st.write("Downloading Model...")
    weights_dir = 'weights'
    model_file = f"{model_name}.pth"
    model_path = os.path.join(weights_dir, model_file)

    #Make directory if file doesn't exist
    if not os.path.exists(weights_dir):
        os.makedirs(weights_dir)

    if not os.path.isfile(model_path):
        if model_name == 'General':
            file_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
        elif model_name == 'Anime':
            file_url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth'
        model_path = load_file_from_url(
            url=file_url, model_dir=weights_dir, progress=True, file_name=model_file)
    return model_path

def app():
    # Streamlit app
    st.title(":orange[EnhanceAI] 🐱‍💻✨")

    uploaded_file = st.file_uploader("Choose an image", accept_multiple_files=False, type=["jpg", "png", "jpeg"],
                                    help="An image that have big size will take more time to complete image enhancment")
    
    if uploaded_file is not None:
        # Save uploaded image to disk
        input_image_path = os.path.join("temp", "input_image.png")
        os.makedirs("temp", exist_ok=True)
        with open(input_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    # User selects model name
    model_name = st.selectbox("Image Type", ['General', 'Anime'])

    # User login or not
    user = get_user_session_state()
    if user is None or user == "user":
        advanceDisabled = st.session_state.disabled = True
    else:
        advanceDisabled = st.session_state.disabled = False
    
    # User selects advances parameters
    on = st.toggle("Advance features", disabled=advanceDisabled, help="Login required.")
    if on:
        denoise_strength = st.slider("Denoise Strength", 0.0, 1.0, 0.5, help="Denoise strength. 0 for weak denoise (keep noise), 1 for strong denoise ability.")
        outscale = st.slider("Output Scale", 1, 4, 2, help="The final upsampling scale of the image.")  #Default utput scale to 2
        tile = st.slider("Tile", 64, 512, 256, 64, help="Tile size, 0 for no tile during testing")
        tile_pad = st.slider("Tile Pad", 0, 20, 10, 2, help="Tile padding")
        pre_pad = st.slider("Pre Pad", 0, 10, 0, 2,help="Pre padding size at each border")
        fp32 = st.checkbox("fp32 Precision", value=False, help="Use fp32 precision during inference. Uncheck: fp16 (half precision).")
        face_enhance = st.checkbox("Face Enhance", value=False, help="Use GFPGAN to enhance face")
    else:
        if uploaded_file is not None:
            st.info('Default parameter is applied', icon="ℹ️")
        denoise_strength = 0.5
        outscale = 2
        tile = 256
        tile_pad = 10
        pre_pad = 0
        fp32 = False
        face_enhance = False
    gpu_id = None  #gpu device to use (default=None) can be 0,1,2 for multi-gpu

    col1, col2 = st.columns(2)
    if uploaded_file is not None:
        with col1:
            st.write("### Original Image")
            st.image(uploaded_file, use_column_width=True)

        # Save uploaded image to disk
        input_image_path = os.path.join("temp", "input_image.png")
        os.makedirs("temp", exist_ok=True)
        with open(input_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        runDisabled = st.session_state.disabled = False
    else:
        runDisabled = st.session_state.disabled = True

    with col1:
        startButton = st.button("Start", disabled=runDisabled, help="Start image enhancement.")

    # Start Enhancemnet
    if startButton:
        with st.status("Running...", expanded=True) as status:
            # Ensure model weights are downloaded
            model_path = ensure_model_weights(model_name)
            
            # Load the model
            upsampler = load_model(model_name, model_path, denoise_strength, tile, tile_pad, pre_pad, fp32, gpu_id)

            # Load the image
            img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            
            #Check error  
            if img is None:
                st.error("Error loading image. Please try again.")
            else:
                try:
                    if face_enhance:
                        # Run if Face Enhance Check
                        st.write("Face Enhancing...")
                        st.info('This process may take some time.', icon="ℹ️")
                        face_enhancer = GFPGANer(
                        model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
                            upscale=outscale,
                            arch='clean',
                            channel_multiplier=2,
                            bg_upsampler=upsampler)
                        _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
                    else:
                        #No Face Enhance
                        st.write("Enhancing...")
                        st.info('This process may take some time.', icon="ℹ️")
                        output, _ = upsampler.enhance(img, outscale=outscale)
                except RuntimeError as error:
                    # Error Checking for Enhance
                    st.error(f"Error: {error}")
                    st.error('If you encounter CUDA out of memory, try to set a smaller tile size.')
                else:
                    # Save and display the output image
                    output_image_path = os.path.join("temp", "output_image.png")
                    cv2.imwrite(output_image_path, output)
                    with col2:
                        st.write("### Enhanced Image")
                        st.image(output_image_path, use_column_width=True)
                    status.update(label="Enhancement complete!", state="complete", expanded=False)
                    with col2:
                        if 'output_image_path' in locals():
                            st.download_button("Download Enhanced Image", data=open(output_image_path, "rb").read(), file_name="output_image.png", mime="image/png")
        # Do image comparison side by side
        image_comparison(
            img1="temp/input_image.png",
            img2="temp/output_image.png",
            label1="Before",
            label2="After",
            starting_position=50,
            show_labels=True,
            make_responsive=True,
        ) 

    