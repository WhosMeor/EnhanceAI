import streamlit as st
from streamlit_image_comparison import image_comparison

def app():
    def KAIJUNO8():
         image_comparison(
            img1="images/kaijuno8_input.png",
            img2="images/kaijuno8_output.png",
            label1="Before",
            label2="After",
            starting_position=50,
            show_labels=True,
            make_responsive=True,
        )
    def SENTINELS():
        image_comparison(
            img1="images/sentinels_input.png",
            img2="images/sentinels_output.png",
            label1="Before",
            label2="After",
            starting_position=50,
            show_labels=True,
            make_responsive=True,
        )
    def LEWIS():
        image_comparison(
            img1="images/lewis_input.png",
            img2="images/lewis_output.png",
            label1="Before",
            label2="After",
            starting_position=50,
            show_labels=True,
            make_responsive=True,
        )


    st.title("Image :orange[Enhancement] Web App using :blue[Real-ESRGAN] 🐱‍💻✨")
    images = st.radio("Image Selection",["Kaiju No. 8", "Sentinels", "Lewis Hamilton"], label_visibility="collapsed", horizontal=True, index=0,)
    if images == "Kaiju No. 8":
        KAIJUNO8()
    elif images == "Sentinels":
        SENTINELS()
    else:
        LEWIS()


    st.header(":blue[Introduction]")
    st.write("""
    This project focuses on developing a :orange[web app using Real-ESRGAN for image enhancement]. It aims to :orange[improve the visual quality of low-resolution images] efficiently and cost-effectively.
    """)

    st.header(":blue[Background]")
    st.write("""
    :orange[Image enhancement improves image quality], crucial for computer vision and real-life applications. Traditional methods struggle with complex degradations. :orange[Real-ESRGAN offers a superior solution by enhancing details while minimizing artifacts].
    """)

    st.header(":blue[Problem Statement]")
    st.write("""
    :orange[Degraded images suffer from blurs, noise, and compression]. Specialized hardware is costly. :orange[A web app with Real-ESRGAN can provide accessible, high-quality image enhancement].
    """)

    st.header(":blue[Objectives]")
    st.write("""
    - :orange[Identify techniques for enhancing low-resolution images].
    - :orange[Develop a web app for diverse image types].
    - :orange[Evaluate user satisfaction with the app].
    """)

    st.header(":blue[Scope]")
    st.write("""
    :orange[Focus on low-resolution images using publicly available datasets]. Future expansion to other image types is possible.
    """)

    st.header(":blue[Significance]")
    st.write("""
    The app :orange[offers an affordable solution for enhancing cherished memories]. It advances image enhancement technology and provides valuable insights for future developments.
    """)

    st.header(":blue[Summary]")
    st.write("""
    This project :orange[aims to deliver a user-friendly web app for enhancing low-resolution images], addressing the stated problems and achieving the outlined objectives.
    """)