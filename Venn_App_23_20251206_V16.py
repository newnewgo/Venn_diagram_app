#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Code-V14C
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from matplotlib import font_manager as fm
import os

# =========================================
# 載入中文字型（避免亂碼）
# =========================================
FONT_PATH = "NotoSansTC-Regular.ttf"  # 請確保 ttf 放在同資料夾
if os.path.exists(FONT_PATH):
    prop = fm.FontProperties(fname=FONT_PATH)
else:
    st.error("⚠️ 找不到字型檔 NotoSansTC-Regular.ttf，請將檔案放在程式同目錄。")
    st.stop()

plt.rcParams['font.family'] = prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 負號正常顯示

# =========================================
# Streamlit 頁面設定
# =========================================
st.set_page_config(layout="wide")
st.title("文氏圖產生器")

# =====================
# Sidebar 設定
# =====================
st.sidebar.markdown("## ⚙️ 文氏圖設定")
mode = st.sidebar.radio("選擇文氏圖類型：", ["2 圓", "3 圓"])

st.sidebar.markdown("## 🎨 顯示設定")
show_labels = st.sidebar.checkbox("顯示集合標籤（A/B/C）", value=True)
show_values = st.sidebar.checkbox("顯示區塊數字", value=True)
st.sidebar.markdown("## 📏 圖片大小設定")
fig_size = st.sidebar.slider("圖寬 / 圖高 (inch)", 3.0, 10.0, 5.0, step=0.5)

st.markdown("### 圖表標題（可留空）")
chart_title = st.text_input("", value="")

# =====================
# 2 圓 Venn
# =====================
if mode == "2 圓":
    st.header("2 圓文氏圖")
    col1, col2 = st.columns(2)
    with col1:
        setA_size = st.number_input("集合 A 大小", min_value=0, value=30)
        setA_color = st.color_picker("集合 A 顏色", "#FFAAC0")
    with col2:
        setB_size = st.number_input("集合 B 大小", min_value=0, value=20)
        setB_color = st.color_picker("集合 B 顏色", "#C6AFE9")
    intersection = st.number_input("交集大小", min_value=0, value=10)

    if intersection > min(setA_size, setB_size):
        st.error("❌ 交集不能大於任一集合大小")
    else:
        fig, ax = plt.subplots(figsize=(fig_size, fig_size))
        v = venn2(subsets=(setA_size - intersection, setB_size - intersection, intersection),
                  set_labels=("集合 A", "集合 B") if show_labels else ("", ""),
                  ax=ax)

        # Set 顏色
        if v.get_patch_by_id("10"):
            v.get_patch_by_id("10").set_color(setA_color)
            v.get_patch_by_id("10").set_alpha(0.6)
        if v.get_patch_by_id("01"):
            v.get_patch_by_id("01").set_color(setB_color)
            v.get_patch_by_id("01").set_alpha(0.6)
        if v.get_patch_by_id("11"):
            from matplotlib_venn import venn2
            def mix_colors(*colors):
                rgb_list = []
                for c in colors:
                    c = c.lstrip("#")
                    rgb = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
                    rgb_list.append(rgb)
                avg_rgb = tuple(sum(channel) // len(rgb_list) for channel in zip(*rgb_list))
                return "#{:02X}{:02X}{:02X}".format(*avg_rgb)
            v.get_patch_by_id("11").set_color(mix_colors(setA_color, setB_color))
            v.get_patch_by_id("11").set_alpha(0.55)

        # 顯示/隱藏數字
        if not show_values:
            for t in v.subset_labels:
                if t: t.set_text("")
        # 顯示/隱藏標籤
        if not show_labels:
            for t in v.set_labels:
                if t: t.set_text("")
        else:
            # 調整標籤字型
            if v.set_labels[0]: 
                v.set_labels[0].set_fontproperties(prop)
            if v.set_labels[1]: 
                v.set_labels[1].set_fontproperties(prop)
            # 調整數字字型
            if v.subset_labels:
                for t in v.subset_labels:
                    if t: t.set_fontproperties(prop)

        if chart_title.strip():
            plt.title(chart_title, fontproperties=prop)
        st.pyplot(fig)

# =====================
# 3 圓 Venn
# =====================
else:
    st.header("3 圓文氏圖")
    col1, col2, col3 = st.columns(3)
    with col1:
        a_size = st.number_input("集合 A 大小", min_value=0, value=40)
        a_color = st.color_picker("集合 A 顏色", "#FFAAC0")
    with col2:
        b_size = st.number_input("集合 B 大小", min_value=0, value=35)
        b_color = st.color_picker("集合 B 顏色", "#C6AFE9")
    with col3:
        c_size = st.number_input("集合 C 大小", min_value=0, value=30)
        c_color = st.color_picker("集合 C 顏色", "#99CC99")

    st.subheader("交集設定")
    colA, colB, colC = st.columns(3)
    with colA:
        ab = st.number_input("AB 交集", min_value=0, value=10)
    with colB:
        ac = st.number_input("AC 交集", min_value=0, value=8)
    with colC:
        bc = st.number_input("BC 交集", min_value=0, value=6)
    abc = st.number_input("ABC 三者交集", min_value=0, value=3)

    if abc > min(ab, ac, bc):
        st.error("❌ ABC交集不得大於任兩集合交集")
    else:
        fig, ax = plt.subplots(figsize=(fig_size, fig_size))
        v = venn3(subsets=(a_size, b_size, ab, c_size, ac, bc, abc),
                  set_labels=("集合 A", "集合 B", "集合 C") if show_labels else ("", "", ""),
                  ax=ax)
        # Set 顏色
        if v.get_patch_by_id("100"): v.get_patch_by_id("100").set_color(a_color)
        if v.get_patch_by_id("010"): v.get_patch_by_id("010").set_color(b_color)
        if v.get_patch_by_id("001"): v.get_patch_by_id("001").set_color(c_color)
        # 交集自動灰色透明
        patch_colors = {
            "110": mix_colors(a_color, b_color),
            "101": mix_colors(a_color, c_color),
            "011": mix_colors(b_color, c_color),
            "111": mix_colors(a_color, b_color, c_color)
        }
        for patch_id, color in patch_colors.items():
            patch = v.get_patch_by_id(patch_id)
            if patch:
                patch.set_color(color)
                patch.set_alpha(0.55)

        # 顯示/隱藏數字
        if not show_values:
            for t in v.subset_labels:
                if t: t.set_text("")
        # 顯示/隱藏標籤
        if not show_labels:
            for t in v.set_labels:
                if t: t.set_text("")
        else:
            # 調整標籤字型
            if v.set_labels[0]: v.set_labels[0].set_fontproperties(prop)
            if v.set_labels[1]: v.set_labels[1].set_fontproperties(prop)
            if v.set_labels[2]: v.set_labels[2].set_fontproperties(prop)
            # 調整數字字型
            if v.subset_labels:
                for t in v.subset_labels:
                    if t: t.set_fontproperties(prop)

        if chart_title.strip():
            plt.title(chart_title, fontproperties=prop)
        st.pyplot(fig)

