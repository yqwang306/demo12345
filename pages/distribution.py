import streamlit as st
from retrieval import *
from dialogue import *

st.set_page_config(page_title="智能派单", page_icon="🌍")

st.markdown("# 智能派单")
st.sidebar.header("智能派单")

# 使用“with”语法添加单选按钮
with st.sidebar:
    add_radio = st.radio(
        "选择一种算法",
        ("基于事理图谱", "基于检索", "基于大模型")
    )

if add_radio == "基于检索":
    retrieval_main()
    # dialogue()