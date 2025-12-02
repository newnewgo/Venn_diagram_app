#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

st.set_page_config(layout="wide")

st.title("Venn Diagram 產生器｜2 圓 / 3 圓")

st.sidebar.markdown("## ⚙️ 設定")
mode = st.sidebar.radio("選擇文氏圖類型", ["2 圓 Venn", "3 圓 Venn"])


# =====================
# 通用顯示設定
# =====================
st.sidebar.markdown("## 🎨 顯示設定")

show_labels = st.sidebar.checkbox("顯示 Set 標籤（Set1 / Set2 / Set3）", value=True)
show_values = st.sidebar.checkbox("顯示區塊數字", value=True)

st.markdown("### 圖表標題（可選填）")
chart_title = st.text_input("（可留空）", value="")


# =====================
# 2 圓 Venn
# =====================
if mode == "2 圓 Venn":
    st.header("🔵 2 圓 Venn Diagram")

    col1, col2 = st.columns(2)
    with col1:
        set1_size = st.number_input("Set 1 大小", min_value=0, value=30)
        set1_color = st.color_picker("Set 1 顏色", "#FF9999")

    with col2:
        set2_size = st.number_input("Set 2 大小", min_value=0, value=20)
        set2_color = st.color_picker("Set 2 顏色", "#9999FF")

    intersection = st.number_input("交集大小", min_value=0, value=10)

    # 防呆
    if intersection > min(set1_size, set2_size):
        st.error("❌ 交集不能大於任一集合大小")
    else:
        fig, ax = plt.subplots(figsize=(5, 5))

        v = venn2(
            subsets=(set1_size - intersection, set2_size - intersection, intersection),
            set_labels=("Set1", "Set2") if show_labels else ("", ""),
            ax=ax
        )

        # 顏色
        if v.get_patch_by_id("10"):
            v.get_patch_by_id("10").set_color(set1_color)
            v.get_patch_by_id("10").set_alpha(0.6)

        if v.get_patch_by_id("01"):
            v.get_patch_by_id("01").set_color(set2_color)
            v.get_patch_by_id("01").set_alpha(0.6)

        if v.get_patch_by_id("11"):
            # 自動生成交集顏色（以灰色透明代替混色）
            v.get_patch_by_id("11").set_color("#BBBBBB")
            v.get_patch_by_id("11").set_alpha(0.5)

        # 控制區塊數字
        if not show_values:
            for t in v.subset_labels:
                if t:
                    t.set_text("")

        # 控制 Set 標籤
        if not show_labels:
            for t in v.set_labels:
                if t:
                    t.set_text("")

        # 標題（可留空）
        if chart_title.strip() != "":
            plt.title(chart_title)

        st.pyplot(fig)



# =====================
# 3 圓 Venn
# =====================
else:
    st.header("🔵 3 圓 Venn Diagram")

    col1, col2, col3 = st.columns(3)

    with col1:
        a_size = st.number_input("Set A 大小", min_value=0, value=40)
        a_color = st.color_picker("Set A 顏色", "#FF9999")
    with col2:
        b_size = st.number_input("Set B 大小", min_value=0, value=35)
        b_color = st.color_picker("Set B 顏色", "#9999FF")
    with col3:
        c_size = st.number_input("Set C 大小", min_value=0, value=30)
        c_color = st.color_picker("Set C 顏色", "#99CC99")

    st.subheader("交集設定（請不要讓交集大於原集合）")
    colA, colB, colC = st.columns(3)

    with colA:
        ab = st.number_input("AB 交集", min_value=0, value=10)
    with colB:
        ac = st.number_input("AC 交集", min_value=0, value=8)
    with colC:
        bc = st.number_input("BC 交集", min_value=0, value=6)

    abc = st.number_input("ABC 三者交集", min_value=0, value=3)

    # 防呆
    if abc > min(ab, ac, bc):
        st.error("❌ ABC（三交集）不得大於任兩集合交集")
    else:
        fig, ax = plt.subplots(figsize=(7, 7))

        v = venn3(
            subsets=(a_size, b_size, ab, c_size, ac, bc, abc),
            set_labels=("A", "B", "C") if show_labels else ("", "", ""),
            ax=ax
        )

        # 顏色（Set 顏色）
        if v.get_patch_by_id("100"): v.get_patch_by_id("100").set_color(a_color)
        if v.get_patch_by_id("010"): v.get_patch_by_id("010").set_color(b_color)
        if v.get_patch_by_id("001"): v.get_patch_by_id("001").set_color(c_color)

        # 交集區域 → 自動灰色透明呈現
        for patch_id in ["110", "101", "011", "111"]:
            patch = v.get_patch_by_id(patch_id)
            if patch:
                patch.set_color("#BBBBBB")
                patch.set_alpha(0.5)

        # 不顯示數字
        if not show_values:
            for t in v.subset_labels:
                if t:
                    t.set_text("")

        # 不顯示 Set 標籤
        if not show_labels:
            for t in v.set_labels:
                if t:
                    t.set_text("")

        # 標題（可留空）
        if chart_title.strip() != "":
            plt.title(chart_title)

        st.pyplot(fig)


# In[ ]:




