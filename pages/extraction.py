import streamlit as st
import pandas as pd
import jieba
from wordcloud import WordCloud

st.set_page_config(page_title="热点抽取", page_icon="🌍")


# 使用大模型抽取问题描述中的关键词，包括投诉对象、投诉原因以及意见等，保存在txt文件中
def extract(data):
    return 0


def display(upload):
    data = pd.read_excel(upload)
    extract(data)
    
    complaint_object = []
    complaint_cause = []
    advice = []
    with open("extract_res_qwen7b.txt", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split(" ")
            if '无' not in line[0]:
                complaint_object.append(line[0])
            if '无' not in line[1]:
                complaint_cause.append(line[1])
            if '无' not in line[2]:
                advice.append(line[2])
    
    
    complaint_object = " ".join(complaint_object)
    wc1 = WordCloud(font_path="C:\Windows\Fonts\STSONG.TTF", collocations=False, 
    width=800, height=400, margin=2, background_color='white').generate(complaint_object.lower())

    complaint_cause = " ".join(complaint_cause)
    wc2 = WordCloud(font_path="C:\Windows\Fonts\STSONG.TTF", collocations=False, 
    width=800, height=400, margin=2, background_color='white').generate(complaint_cause.lower())

    advice = " ".join(advice)
    wc3 = WordCloud(font_path="C:\Windows\Fonts\STSONG.TTF", collocations=False, 
    width=800, height=400, margin=2, background_color='white').generate(advice.lower())

    col1, col2, col3 = st.columns(3)
    
    col1.image(wc1.to_array(), caption='投诉对象')
    col2.image(wc2.to_array(), caption='投诉原因')
    col3.image(wc3.to_array(), caption='诉求')

                
def word_cloud():
    st.write("# 热点抽取")
    st.write(
        ":point_right: 给定一段时间内的投诉数据，抽取问题描述中的关键词，包括投诉对象、投诉原因以及诉求等，通过可视化图表的方式进行展示，帮助寻找近期热点事件。"
    )

    my_upload = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "xls"])
    if my_upload is not None:
        display(my_upload)


if __name__ == "__main__":
    word_cloud()