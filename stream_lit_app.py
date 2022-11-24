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


text=st.text_input("Enter a value")
response= requests.get('http://localhost:8000/search_tags?search_tag='+text)
display_img([response.json()[i] for i in response.json()])




