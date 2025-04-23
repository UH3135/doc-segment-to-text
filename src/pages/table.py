import streamlit as st
import streamlit.components.v1 as components

from parsers.table_parser import TableParser
from utils.logger import init_logger


logger = init_logger(__file__, "DEBUG")

if 'table_parser' not in st.session_state:
    st.session_state.table_parser = TableParser()

html_string = None

st.title("Table to JSON")

uploaded_file = st.file_uploader("HTML 파일을 업로드 하세요", type=["html"])
if uploaded_file is not None:
    try:
        html_string = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        st.error("올바른 UTF-8 형식의 HTML 파일을 업로드해주세요.")
    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
if st.button("json 변환"):
    if html_string:
        with st.spinner("json 변환 중입니다..."):
            json_data = st.session_state.table_parser.parse_table_from_html(html_string) 

        st.write("업로드된 JSON 데이터:")
        st.json(json_data)
    else:
        st.warning("HTML 파일을 먼저 업로드해주세요.")

