---
# =========================================
# YAML Front Matter
# ===========================================
title: Python 在業務上的應用
author: 俞欣榮
date: 2024年8月
institute: 中央銀行經濟研究處
theme: black          # reveal.js 主題：black / white / moon / solarized / sky
slideNumber: true     # 顯示投影片頁碼
transition: slide     # 切換動畫：slide / fade / convex / none
# pandoc 1_intro.md -t revealjs -o Intro.html --embed-resources --standalone --slide-level=2 -V theme=black -V revealjs-url=https://unpkg.com/reveal.js@4.6.1
#
---

<!-- === -->
 

## 本節課程大綱

- 央行為何要關注不動產市場
- Python 在資料處理上的應用
- 實際案例：實價登錄資料庫的處理
- 課程大綱與時間安排
- 各節重點預覽
- 課程結語


## 為什麼學 Python？

<!-- 這頁列出業務痛點，用無序清單 -->

在日常業務中，我們經常面對以下挑戰：

- 大量結構化資料（CSV、Excel）需要定期整理與彙整
- 檔案命名規則複雜，需從路徑或檔名中萃取資訊
- 資料清理耗費大量人工，且容易出錯
- 重複性的統計工作難以自動化

<!-- **文字** → 粗體；*文字* → 斜體 -->
**過去的做法**往往是手動操作 Excel、逐筆比對資料，費時且難以重現。


## 實際案例：實價登錄

<!-- > 開頭 → 引用區塊（blockquote），視覺上會縮排並有左側色條 -->

> 每期公布的壓縮檔內含數十個以縣市代碼與交易類別命名的 CSV 檔案
> （如 `a_a.csv`、`f_b.csv`）

<!-- `文字` → 行內程式碼（inline code），會用等寬字型顯示 -->
<!-- 有序清單：用數字加句點開頭 1. 2. 3. -->

透過 Python，我們能夠：

1. **自動辨識**所有符合規則的檔案（`pathlib.Path`）
2. **批次讀取與彙整**全國各縣市資料（`pandas`）
3. **從檔名中萃取**縣市代碼與交易類別（`re` 正則表達式）
4. **進行數值運算與統計**（`numpy`）
5. 最終完成可重現、可更新的分析流程


## 課程大綱（約 2 小時）

<!-- 表格語法：
  - 第一行是標題列
  - 第二行是對齊設定：:--- 靠左、:---: 置中、---: 靠右
  - 之後每行是資料列，欄位用 | 分隔 -->

| 節次 | 主題 | 時間 |
|:---:|:---|:---:|
| 1 | **課程簡介與動機** | 25 分鐘 |
| — | 休息 | 10 分鐘 |
| 2 | **pandas**：讀取、篩選、彙整資料 | 25 分鐘 |
| — | 休息 | 10 分鐘 |
| 3 | **re + numpy**：文字萃取與數值運算 | 25 分鐘 |
| — | 休息 | 10 分鐘 |
| 4 | **pathlib.Path + 綜合實作** | 25 分鐘 |
| — | QA | 10 分鐘 |


## 📦 Lecture 2：pandas 重點

- 讀取 CSV / Excel 檔案
- 資料篩選（`loc`、`query`）
- 分組統計（`groupby`）
- 多檔合併（`concat`、`merge`）

<!-- 程式碼區塊：用三個反引號包起來，後面加語言名稱會有語法高亮 -->

```python
import pandas as pd

df = pd.read_csv("a_a.csv")
df.head()
```


## 🔍 Lecture 3：正則表達式（re）

- 基本語法：`[]`、`*`、`+`、`?`、`()`
- 從檔名中萃取縣市代碼與交易類別
- 資料欄位中的文字清理

```python
import re

filename = "a_a.csv"
match = re.match(r"([a-z]+)_([a-z]+)\.csv", filename)
print(match.group(1))  # 縣市代碼
print(match.group(2))  # 交易類別
```


## 🔢 Lecture 3：numpy 重點

- 陣列建立與基本運算
- 統計函數（`mean`、`std`、`percentile`）
- 與 pandas 的搭配使用

```python
import numpy as np

prices = np.array([1500, 2000, 3500, 8500, 12000])
print(np.mean(prices))
print(np.percentile(prices, 75))
```


## 📁 Lecture 4：pathlib.Path 重點

- 路徑的表示與操作
- 列出資料夾下所有檔案（`glob`）
- 根據命名規則篩選目標檔案

```python
from pathlib import Path

data_dir = Path("data/")

# 找出所有成屋交易合計檔案（*_a.csv）
files = list(data_dir.glob("*_a.csv"))
print(files)
```


## 課程結語：回到業務現場

> 假設你收到了一份新的實價登錄壓縮檔，裡面有數十個依縣市與交易類別命名的 CSV 檔案。
> 你能用今天學到的工具，在 **10 分鐘內**完成全國成屋交易資料的彙整與基礎統計嗎？

<!-- 水平線：三個以上的 --- 或 *** -->
---

**答案是可以的。** 讓我們開始吧 🚀

 
