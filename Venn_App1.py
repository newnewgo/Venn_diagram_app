#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install matplotlib-venn


# In[2]:


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

    # 繪製文氏圖
    venn2(subsets=(set1_only, set2_only, intersection_size), set_labels=('Set 1', 'Set 2'))

    # 顯示圖表
    plt.show()

# 範例：
set1_size = 30
set2_size = 20
intersection_size = 10

draw_venn_from_sizes(set1_size, set2_size, intersection_size)


# In[ ]:




