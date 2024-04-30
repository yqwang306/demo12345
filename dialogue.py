import streamlit as st
import faiss
import pandas as pd
import re
import numpy as np
from sentence_transformers import SentenceTransformer

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

def is_Chinese(word):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    if pattern.search(word):
        return False
    else:
        return True

def dialogue():
    st.write("## 基于检索")
    st.write(
        ":point_right: 基于检索的智能派单。模型会从历史数据中检索出语义最相似的topK个问题描述，并根据其主责部门进行新工单的派发。"
    )

    topk = st.sidebar.slider(
        '检索前K个相似样本',
        0, 20, 10      
    )

    # with st.chat_message("user"):
    #     problem = st.chat_input("请输入问题描述")

    if problem := st.chat_input("请输入问题描述"):
        # 在页面上显示用户的输入
        with st.chat_message("user"):
            st.markdown(problem)

        if problem is not None:

            model = SentenceTransformer('/data2/yh/model/acge_text_embedding/')
            history_problems, history_labels = get_labels("data.xlsx")
            index = faiss.read_index("./index_file.index")

            embedding = model.encode(problem, normalize_embeddings=True)
            embedding = np.array([embedding])
            
            values, idxs = index.search(embedding, topk)

            res_retrieval = pd.DataFrame(columns = ['问题描述', '三级主责部门', '语义相似度'])
            for i in range(topk):
                res_retrieval.loc[i] = [history_problems[idxs[0][i]], history_labels[idxs[0][i]], values[0][i]]
            res_retrieval.index = res_retrieval.index + 1
            st.write(res_retrieval)

