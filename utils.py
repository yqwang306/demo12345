import streamlit as st
import pandas as pd

def read_data():
    uploaded_file = st.file_uploader("上传文件", type=["xlsx", "csv"])

    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        problems = list(data['问题描述'])
        labels = list(data['三级主责部门'])

    return problems, labels