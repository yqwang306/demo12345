import pandas as pd
import streamlit as st

def read_excel(file_path):
    data = pd.read_excel(file_path)
    return data

def classify():
    data = read_excel('data.xlsx')
    problems = list(data['问题描述'])
    labels = list(data['三级主责部门'])

    for i in range(len(labels)):
        if pd.isnull(labels[i]):
            labels[i] = "空"
        if "街道" in labels[i]:
            labels[i] = "街道"

    types = set(labels)
    types.remove("空")

    for i in range(len(labels)):
        if pd.isnull(labels[i]):
            del labels[i]
            del problems[i]


    from transformers import AutoTokenizer, AutoModel

    tokenizer = AutoTokenizer.from_pretrained("/data2/gm/model/chatglm-6b/", trust_remote_code=True)
    model = AutoModel.from_pretrained("/data2/gm/model/chatglm-6b/", trust_remote_code=True).half().cuda()
    model = model.eval()

    demos = ""
    has_add = []
    for i in range(32):
        has_add.append(labels[i])
        demos += f"案件描述：{problems[i]}\n应该被委派到：{labels[i]}\n"

    prompt = f"给定主责部门选项：\n{str(types)}\n请根据以下的案件描述，判断该案件应该被委派到哪一个主责部门。请只给出选择的结果。"
    user_prompt = st.chat_input("请输入问题描述")
    problem = st.chat_message("user").write(user_prompt)
    prompt = prompt + "以下是一些示例：\n" + demos + f"\n案件描述：{problem}\n应该被委派到："
    response, _ = model.chat(tokenizer, prompt, history=[], num_beams=4, do_sample=False)
    st.chat_message("assistant").write(response)
