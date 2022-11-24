
import streamlit as st
import requests
from PIL import Image
import base64
import io
def display_img(img_list):
    for i in img_list:
        msg = base64.b64decode(i)
        buf = io.BytesIO(msg)
        img = Image.open(buf)
        st.image(img, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")



def main_page():
    st.title("Upload Page")
    uploaded_file=st.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        res = requests.post(url='http://localhost:8000/upload_image',
                    data=bytes_data,
                    headers={'Content-Type': 'application/octet-stream'})
        print(res.status_code)

def search_image_page():
    st.title("Search images page")
    text=st.text_input("Enter a value")
    response= requests.get('http://localhost:8000/search_tags?search_tag='+text)
    display_img([response.json()[i] for i in response.json()])


page_names_to_funcs = {
    "Upload image page": main_page,
    "Search images page": search_image_page,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()