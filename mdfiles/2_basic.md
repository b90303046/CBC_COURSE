---
# =========================================
# YAML Front Matter
# ===========================================
title: 運用Python進行資料清理之實務操作： 
subtitle: 基本Python介紹

author: 俞欣榮
date: 2024年8月
institute: 中央銀行經濟研究處
theme: white          # reveal.js 主題：black / white / moon / solarized / sky
slideNumber: true     # 顯示投影片頁碼
transition: slide     # 切換動畫：slide / fade / convex / none
---
 
## 本節課程大綱(基本Python介紹)

1. Python直譯器是什麼（計算機類比）
2. 兩種執行方式（Shell vs Colab/Jupyter）
3. 基本型態：`int`、`float`、`str`、`list`、`dict`
4. 函式概念（callable vs 變數，type hint簡介）
5. `for` 迴圈 + `if` 條件判斷




## 甚麼是Python ?

::: {style="display: flex; gap: 3rem; align-items: flex-start;"}

::: {style="flex: 1;"}

**傳統計算機**

- 打 `2 + 2`，得到 `4`
- 打 `5 * 5`，得到 `25`
- 輸入指令 → 立即回應
**Python 直譯器**
```python
>>> 2 + 2
4
>>> 5 * 5
25
>>> "中央銀行" + "經濟研究處" # 字串處理
'中央銀行經濟研究處'
```
:::
 
::: {style="flex: 0.8; display: flex; align-items: right;"}
<img src="mdfiles/calculator.png" style="width: 120%;">
:::

:::

## Python的本質

`Python` 和 `R`、`Matlab`一樣，屬於**直譯器**語言——輸入指令，立即執行，不需要事先編譯。

Python 能做計算機做不到的事(舉例)
```python
# 1. 儲存結果
x = 2 + 2
# 2. 處理文字
name = "實價登錄"
#3. 處理整批資料
prices = [1500, 2300, 1800, 2100]
for p in prices:
    print(p * 0.9)
```
**Python 直譯器才是核心**，Jupyter、VS Code 只是協助寫程式、管理檔案的介面。
- 和VBA比較

| VBA | Python  |
|:---|:---|
| Excel 計算引擎 | Python 直譯器 |
| VBA 編輯器 | VS Code / Jupyter / Colab |
| `.bas` 模組檔 | `.py` 程式檔 | 


## 兩種執行方式

::: {style="display: flex; gap: 3rem; align-items: flex-start;"}


::: {style="flex: 1;"}

**方式一：直譯器（終端機）**

直接在終端機啟動，逐行執行，即時回應

```powershell
# 在終端機輸入
python

# 進入互動介面後
>>> print("Hello, World!")
Hello, World!
>>> 1 + 1
2
```

- 最接近 Python 本質的操作方式
- 適合快速測試單行指令
- 了解直譯器如何「讀一行、跑一行」
- 程式碼存為 `.py`，可直接重複執行
:::
 
::: {style="flex: 1;"}

**方式二：Colab / Jupyter Lab**

在瀏覽器(Chrome, Edge)裡執行，以格子(Cell)為單位

- 畫面友善，適合邊寫邊看結果
- 背後其實是 **IPython**（Python 的強化版互動介面）
- Cell 的概念是 IPython 加上的，不是 Python 原生的
- 程式碼存為 `.ipynb`，格子與輸出結果一起儲存
:::

:::

## 互動介面實例(Python Shell)

**Python Shell**
<img src="mdfiles/shell.png" style="width: 100%;">

- 在Windows電腦開啟Powershell後輸入`Python` 
- 進入環境後, 可輸入`exit()`離開


## 互動介面實例(Colab)

<img src="mdfiles/colab.png" style="width: 100%;">

- 直接在google輸入"colab"後登入使用



## Python基本型態

- Python中，每一個變數都有屬於自己的型態，各種型態的屬性也不同
- 比如數字類的變數可以進行運算，文字類的變數可以搜尋與取出，陣列類的變數可以進行迭代
- 各有各自合法運算和處理的功能
- 可以運用指令`type()`去檢視這個變數的型態

Python 最常用的五種型態：

| 型態 | 說明 | 例子 | 對應Excel|
|:---|:---|:---|:---|
| `int` | 整數 | `count = 236` | 儲存格格式 |
| `float` | 小數 | `area = 32.5` | 儲存格格式|
| `str` | 文字字串 | `name = "實價登錄"` |儲存格格式|
| `list` | 有序清單 | `prices = [1500, 2300, 1800]` | 一列資料 |
| `dict` | 鍵值對應 | `{"縣市": "台北市", "總價": 1500}` | 特定欄位 |

**補充**

- 上述的變數型態，是資料內最常見的組成(大家可以回想Excel表)
- 在python的環境中, Excel表是以pandas.DataFrame呈現


## int、float、str

```python
# int：整數
year  = 2024 
count = 236

# float：小數（坪數、價格常用）
area  = 32.5
price = 1500.0

# str：文字
name = "實價登錄"
city = "臺北市"

# 型態轉換
int(32.5)       # 32     （小數 → 整數，直接截斷）
float(1500)     # 1500.0
str(2024)       # "2024"
```

- **注意字串與數值無法進行運算**


## list：有序清單

**`list` 是 Python 最常用的資料結構**

```python
prices = [1500, 2300, 1800, 2100, 'a','b','c']

# 取值：從 0 開始數（不是從 1）
prices[0]    # 1500  ← 第一個
prices[-1]   # 'c'  ← 最後一個

# 切片
prices[1:3]  # [2300, 1800]
# 新增
prices.append(1950)
# 長度
len(prices)  # 5
# 巢狀list 
table = [
    ["台北市", 7000],
    ["新北市", 6000],
    ["其他", 4000]
]
```

- list：可以裝不同型態
- Python 的第一個數字是從`0`開始——這是最常踩的坑

 

## dict：鍵值對應

`dict` 類似R的 `named list`，用名稱（key）來取值，不用記位置。

```python
record = {
    "縣市":   "台北市",
    "鄉鎮市區": "大安區",
    "總價":   1500,
    "坪數":   32.5
}

# 取值：用 key
record["縣市"]   # "台北市"
record["總價"]   # 1500

# 新增或修改
record["單價"] = record["總價"] / record["坪數"]

# 列出所有 key
record.keys()
```

**`dict` 的key必須是唯一。若重複，後面的會覆蓋先前的結果**

 
