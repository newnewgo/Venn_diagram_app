#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

def draw_venn_from_sizes(set1_size, set2_size, intersection_size):
    """
    根據集合大小和交集大小繪製文氏圖。

    參數：
    set1_size: 第一個集合的大小。
    set2_size: 第二個集合的大小。
    intersection_size: 兩個集合的交集大小。
    """
    # 計算各區域的大小
    set1_only = set1_size - intersection_size
    set2_only = set2_size - intersection_size

    # 建立 figure
    fig, ax = plt.subplots()

    # 繪製文氏圖到 ax
    venn2(subsets=(set1_only, set2_only, intersection_size),
          set_labels=('Set 1', 'Set 2'),
          ax=ax)

    # 用 Streamlit 顯示圖表
    st.pyplot(fig)


# Streamlit UI
st.title("Venn Diagram Example")

set1_size = st.number_input("Set 1 size", value=30, min_value=0)
set2_size = st.number_input("Set 2 size", value=20, min_value=0)
intersection_size = st.number_input("Intersection size", value=10, min_value=0)

draw_venn_from_sizes(set1_size, set2_size, intersection_size)

