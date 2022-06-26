from PIL import UnidentifiedImageError
import streamlit as st
import base64
from io import BytesIO

from obj_det import MangoDetect


# page title config
st.set_page_config(page_title="FRU-IT", page_icon="./img/favicon.png")

#open css file
css_path = './static/CSS/style.css'
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# title
with st.container():
    # st.write("""
    #     # FRU-IT 🥭
    #     ### Your personal fruit companion
    # """)
    st.markdown("<h1 style='text-align: center; color: white;'>FRUIT 🥭</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: gray;'>Your personal fruit companion</h2>", unsafe_allow_html=True)


def display_img(img_path):
    st.image(img_path, use_column_width=True)


def ripeness_detection(img_path):
    message, output, opmsg = MangoDetect.detect_ripeness(img_path)
    return message, output, opmsg

def display_output(output):
    st.image(output, width=300, use_column_width=True)

def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


with st.container():
    # file open dialog and function
    
    st.markdown("""---""")
    img_path = st.file_uploader("Upload the image of the mango 🥭", type=["jpg", "png", "jpeg"])
    if img_path is not None:
        st.success("Image uploaded successfully")
        display_img(img_path)
    st.markdown("""---""")
    if st.checkbox('Use camera input'):    
        img_path = st.camera_input(label="Take a photo 📷")
            # button to run ripeness_detection()
        st.markdown("""---""")
    
        if img_path is not None:
            st.success("Image uploaded successfully")
            display_img(img_path)

    st.markdown("""---""")
    if img_path is not None:
        if st.button("Detect Ripeness", help="Click to detect the ripeness of the mango"):
            st.markdown("""---""")
            message, output, opmsg = ripeness_detection(img_path)
            # st.metric(label="", value=message) # here
            st.markdown(f"<h6 style='text-align: center; color: gray;'>{message}</h6>", unsafe_allow_html=True)

            st.markdown("""---""")
            if output is not None:
                st.markdown("<h4 style='text-align: center; color: gray;'>Processed Image 🖼️</h4>", unsafe_allow_html=True)
                if opmsg == "High chances of decay":
                    st.markdown(f"<h6 style='text-align: center; color: red;'>{opmsg} ☹️</h6>", unsafe_allow_html=True)
                elif opmsg == "Possible decay":
                    st.markdown(f"<h6 style='text-align: center; color: yellow;'>{opmsg} 🙂</h6>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h6 style='text-align: center; color: green;'>{opmsg} 😀</h6>", unsafe_allow_html=True)


                st.markdown("""---""")
                try:
                    display_output(output)
                    st.markdown("""---""")
                    st.markdown(get_image_download_link(output,'detect.jpg', "Download the image 💽"), unsafe_allow_html=True)
                    st.markdown("""---""")
                except UnidentifiedImageError:
                    st.warning("No Decay detected! 🤔")
                
                except AttributeError:
                    st.warning("Error Processing the download link")