import base64
import streamlit as st
from PIL import Image

from parsers.image_ocr import ImageOCR
from utils.logger import init_logger

if 'image_ocr' not in st.session_state:
    st.session_state.image_ocr = ImageOCR()

logger = init_logger(__file__, "DEBUG")


st.title("이미지 OCR 추출기")
image_text = None

uploaded_file = st.file_uploader("이미지를 업로드 하세요", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    encode_image = base64.b64encode(file_bytes)
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드한 이미지', use_container_width=True)

if st.button("텍스트 추출"):
    if image is not None:
            with st.spinner("텍스트를 추출 중입니다..."):
                image_text = st.session_state.image_ocr.convert_img_to_txt(encode_image)    

    st.text_area("OCR 결과", image_text, height=200)
