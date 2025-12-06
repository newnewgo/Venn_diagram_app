#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from matplotlib import font_manager as fm
import os

# ---------------------------------------------
# 載入中文字型（避免亂碼）
# ---------------------------------------------
FONT_PATH = "NotoSansTC-Regular.ttf"  # 字型放在同層資料夾
if os.path.exists(FONT_PATH):
    prop = fm.FontProperties(fname=FONT_PATH)
else:
    st.error("⚠️ 找不到字型檔 NotoSansTC-Regular.ttf，請將檔案放在程式同目錄。")
    st.stop()

# ---------------------------------------------
# Streamlit UI 設定
# ---------------------------------------------
st.title("📊 中文維恩圖產生器（支援 2 集合 / 3 集合）")

diagram_type = st.selectbox("選擇圖形類型：", ["2 集合", "3 集合"])

st.subheader("輸入集合區間數字（非數列）")

# 數字輸入區
if diagram_type == "2 集合":
    A = st.number_input("集合 A", min_value=0, value=10)
    B = st.number_input("集合 B", min_value=0, value=8)
    AB = st.number_input("A ∩ B", min_value=0, value=3)
else:
    A = st.number_input("集合 A", min_value=0, value=10)
    B = st.number_input("集合 B", min_value=0, value=8)
    C = st.number_input("集合 C", min_value=0, value=6)
    AB = st.number_input("A ∩ B", min_value=0, value=3)
    AC = st.number_input("A ∩ C", min_value=0, value=2)
    BC = st.number_input("B ∩ C", min_value=0, value=1)
    ABC = st.number_input("A ∩ B ∩ C", min_value=0, value=1)

# 樣式設定
st.subheader("✏️ 標籤樣式設定")

label_font_size = st.slider("標籤字體大小（集合名稱）", 10, 40, 20)
number_font_size = st.slider("區塊數字字體大小", 8, 40, 18)

label_color = st.color_picker("標籤文字顏色", "#000000")
number_color = st.color_picker("區塊數字顏色", "#000000")

# ---------------------------------------------
# 產生圖形
# ---------------------------------------------
if st.button("產生圖形"):

    fig, ax = plt.subplots(figsize=(7, 7))

    if diagram_type == "2 集合":
        subsets = (A - AB, B - AB, AB)
        v = venn2(subsets=subsets, set_labels=("集合 A", "集合 B"), ax=ax)
    else:
        subsets = (
            A - AB - AC + ABC,   # 只屬於 A
            B - AB - BC + ABC,   # 只屬於 B
            AB - ABC,            # A ∩ B（不含 C）
            C - AC - BC + ABC,   # 只屬於 C
            AC - ABC,            # A ∩ C（不含 B）
            BC - ABC,            # B ∩ C（不含 A）
            ABC                  # A ∩ B ∩ C
        )
        v = venn3(subsets=subsets, set_labels=("集合 A", "集合 B", "集合 C"), ax=ax)

    # -----------------------------------------
    # 套用中文字型 + 顏色 + 字體大小
    # -----------------------------------------

    # 集合標籤（A / B / C）
    if v.set_labels:
        for text in v.set_labels:
            if text:
                text.set_fontproperties(prop)
                text.set_fontsize(label_font_size)
                text.set_color(label_color)

    # 區塊內數字
    if v.subset_labels:
        for text in v.subset_labels:
            if text:
                text.set_fontproperties(prop)
                text.set_fontsize(number_font_size)
                text.set_color(number_color)

    st.pyplot(fig)


# In[ ]:




