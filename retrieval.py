import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'


import streamlit as st
import pandas as pd
import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def is_Chinese(word):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    if pattern.search(word):
        return False
    else:
        return True


# 获取历史数据的embeddings和labels
def get_labels(file_path):
    data = pd.read_excel(file_path)
    problems = list(data['问题描述'])
    labels = list(data['三级主责部门'])

    for i in range(len(labels)):
        # 如果是空值
        if pd.isnull(labels[i]):
            labels[i] = "空"
        if "街道" in labels[i]:
            labels[i] = "街道"
    
    i = 0
    while i < len(labels):
        if labels[i] == "空" or is_Chinese(labels[i]) == False: # 存在非中文乱码字符
            del labels[i]
            del problems[i]
        else:
            i += 1
    
    model = SentenceTransformer('/data2/yh/model/acge_text_embedding/')
    
    # # 创建faiss索引
    # d = 1792
    # index = faiss.IndexFlatIP(d)
    # for i in range(0, 800, 100):
    #     sentences = problems[i:i+100]
    #     embeddings = model.encode(sentences, batch_size=32, normalize_embeddings=True)
    #     index.add(embeddings)
    #     print(index.ntotal)
    # faiss.write_index(index, "index_file.index")

    problems = problems[:800]
    labels = labels[:800]
    return problems, labels


# 在历史数据中进行检索，并返回分类结果的dataframe
def retrieval(df, topk):
    problems = list(df['问题描述'])
    index = faiss.read_index("./index_file.index")

    model = SentenceTransformer('/data2/yh/model/acge_text_embedding/')
    history_problems, history_labels = get_labels("data.xlsx")
    
    embeddings = model.encode(problems, batch_size=32, normalize_embeddings=True)
    values, idxs = index.search(embeddings, 20)

    res = pd.DataFrame(columns = ['问题描述', '模型输出结果']) # 用于保存分类结果

    for i in range(len(problems)):
        # 前k个投票
        candi_labels = {}
        for j in range(topk):
            if history_labels[idxs[i][j]] not in candi_labels:
                candi_labels[history_labels[idxs[i][j]]] = values[i][j]
            else:
                candi_labels[history_labels[idxs[i][j]]] += values[i][j]
        
        max_num = 0
        pred_label = ""
        for k, v in candi_labels.items():
            if v > max_num:
                max_num = v
                pred_label = k

        # # 直接使用最相近的label
        # argmax = idxs[i][0]
        # pred_label = history_labels[argmax]

        res.loc[i] = [problems[i], pred_label]
    
    return res


def display(upload, topk):
    data = pd.read_excel(upload)
    st.write("原始数据")
    st.dataframe(data)

    result = retrieval(data, topk)
    
    st.write("模型输出结果")
    st.dataframe(result)


def retrieval_main():
    st.write("## 基于检索")
    st.write(
        ":point_right: 基于检索的智能派单。模型会从历史数据中检索出语义最相似的topK个问题描述，并根据其主责部门进行新工单的派发。"
    )
    st.sidebar.write("## Upload and download :gear:")

    topk = st.sidebar.slider(
        '检索前K个相似样本',
        0, 20, 10      
    )

    my_upload = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "xls"])
    if my_upload is not None:
        display(my_upload, topk)
    