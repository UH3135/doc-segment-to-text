import json
import asyncio
import streamlit as st

from parsers.image_ocr import ImageOCR
from parsers.table_parser import TableParser


if 'image_ocr' not in st.session_state:
    st.session_state.image_ocr = ImageOCR()
    
if 'table_parser' not in st.session_state:
    st.session_state.table_parser = TableParser()


uploaded_file = st.file_uploader("JSON 파일을 업로드하세요", type=["json"], key="file_uploader")

if uploaded_file is not None:
    json_data = json.load(uploaded_file)

    if st.button("텍스트 추출"):
        with st.spinner("텍스트를 추출 중입니다..."):
            for curr_key, curr_json in json_data.items():
                st.session_state.logger.info('complete json loading')

                # table parsing
                table_data = curr_json['tables']
                st.session_state.logger.info('load Table data')
            
                for table_name, table_html in table_data.items():
                    json_data[curr_key]['tables'][table_name] = st.session_state.table_parser.parse_table_from_html(table_html)
    
                # image to text
                image_data = curr_json['images']
                st.session_state.logger.info('load image data')
                
                for image_name, image_byte in image_data.items():
                    try:
                        image_text = st.session_state.image_ocr.convert_img_to_txt(image_byte)
                        json_data[curr_key]['images'][image_name] = image_text
                        st.session_state.logger.info(f"Image {image_name} processed successfully.")
                    except Exception as e:
                        st.session_state.logger.error(f"Error processing image {image_name}: {e}")

    st.write("업로드된 JSON 데이터:")
    st.json(json_data)
