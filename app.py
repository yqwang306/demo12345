import torch, gc

gc.collect()
torch.cuda.empty_cache()

import streamlit as st

st.set_page_config(
    page_title="12345"
)

st.write("# 黄浦区12345 ")

st.sidebar.success("在上方选择一个演示")

st.markdown(
    """
    :one: :orange[智能派单] 根据问题描述，自动将案件派发给对应的部门。\n\n
    :two: :blue[热点抽取] 给定一段时间内的投诉数据，抽取问题描述中的关键词，包括投诉对象、投诉原因以及意见等，通过可视化图表的方式进行展示，帮助寻找近期热点事件。\n\n
    :three: :green[报告生成] 将一天的所有问题描述输入给模型，让模型总结一天的热点问题，并提出相应的建议。
    """
)



