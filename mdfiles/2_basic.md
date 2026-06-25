---
# =========================================
# YAML Front Matter
# ===========================================
title: 運用Python進行資料清理之實務操作： 
subtitle: "內政部不動產交易實價登錄資料之建構、清理與分析<br>基本Python介紹"

author: 俞欣榮
date: 2024年8月
institute: 中央銀行經濟研究處
theme: white          # reveal.js 主題：black / white / moon / solarized / sky
slideNumber: true     # 顯示投影片頁碼
transition: slide     # 切換動畫：slide / fade / convex / none
---
 
## 本節課程大綱

- 安裝與啟動Python環境
  - colab, shell
- Python的基本資料型態
  - list, dict, str, function
- 基本迴圈與練習
- 條件判斷




## 央行為何要關注不動產市場 ?

::: {style="display: flex; gap: 2rem;"}

::: {style="flex: 1;"}
- 中央銀行法第2條：本行經營之目標
  1. 促進金融穩定
  2. 健全銀行業務
  3. 維護對內及對外幣值之穩定
  4. 於上列目標範圍內，協助經濟之發展
- 中央銀行法第39條：**本行為配合金融政策之訂定及其業務之執行，應經常蒐集資料，編製金融統計，辦理金融及經濟研究工作**
- 根據113年國富統計，2024年底國富毛額為330.11 兆元兆元，其中不動產相關近60%
- 另根據本行統計，2025年不動產放款占總放款達 **35%** 以上
- 本行肩負總體與金融穩定政策目標  
  → 完善不動產統計是研擬政策與措施的基石
:::

::: {style="flex: 1; display: flex; align-items: center;"}
<img src="mdfiles/fig1.svg" style="width: 120%;">
:::

:::

## 本科主要不動產相關統計業務資料來源

- 不動產市場動向資料(交易狀態、供給狀態、房價變動、房市展望)
  1. 建物買賣移轉棟數 (成屋交易、第一手交易案件)
  2. **實價登錄統計(住宅交易、預售屋交易/解約、高價住宅)**
  3. 建照執照、建物開工、使用執照統計
  4. 信義房價指數、政大永慶房價指數、內政部住宅價格指數、國泰房價指數、清華安富房價指數
  5. 國泰國民經濟信心調查、永慶房產趨勢前瞻報告、台經院營業氣候測驗點(營建)、中經院營造暨不動產展望...

- 不動產貸款情勢 (選擇性信用管制平台)
  1. 經研處金統科資料
  2. 業務局受限貸款資料
  3. 金檢處相關放款統計(RU01~RU03、法定比率...)
  4. 聯徵中心資料放款資料

- 相關不動產政策統計
  1. 新青安統計
  2. 國際BIS房價所得比資料

⇒ 需定期蒐集資料進行統計，辦理經濟研究相關工作


## 使用Python原因

自2023年初起開始看網路資料和Youtube自學

- 大量結構化資料（CSV、Excel）需要定期整理與彙整
- 資料清理耗費大量人工，且容易出錯
- 我不會VBA



## 個人經驗分享：實價登錄
- 大約2022年開始使用R來進行實價登錄資料的蒐集與彙整 
  - 運用tidyverse, dplyr 等套件 

> 每期公布的壓縮檔內含數十個以縣市代碼與交易類別命名的 CSV 檔案
> （如 `a_a.csv`、`f_b.csv`）

透過 Python，我們能夠：

1. **自動辨識**所有符合規則的檔案（`pathlib.Path`, 正則表達式）
2. **批次讀取與彙整**全國各縣市資料（`pandas`）
3. **從檔名中萃取**縣市代碼與交易類別（`re` 正則表達式）
4. **進行數值運算與統計**（`numpy`）
5. 最終完成可重現、可更新的分析流程


## 課程大綱（約2小時）


| 節次 | 主題 | 時間 |
|:---:|:---|:---:|
| 1 | **課程簡介與動機** | 15 分鐘 |
| 2 | **基本Python介紹** | 15 分鐘|

| 2 | **pandas**：讀取、篩選、彙整資料 | 25 分鐘 |
| 3 | **re + numpy**：文字萃取與數值運算 | 25 分鐘 |
| 4 | **pathlib.Path + 綜合實作** | 25 分鐘 |
| — | QA | 10 分鐘 |


## Lecture 2：pandas 重點

- 讀取 CSV / Excel 檔案
- 資料篩選（`loc`、`query`）
- 分組統計（`groupby`）
- 多檔合併（`concat`、`merge`）


```python
import pandas as pd

df = pd.read_csv("a_a.csv")
df.head()
```


## Lecture 3：正則表達式（re）

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


## Lecture 3：numpy 重點

- 陣列建立與基本運算
- 統計函數（`mean`、`std`、`percentile`）
- 與 pandas 的搭配使用

```python
import numpy as np

prices = np.array([1500, 2000, 3500, 8500, 12000])
print(np.mean(prices))
print(np.percentile(prices, 75))
```


## Lecture 4：pathlib.Path 重點

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



 
## 本節課程大綱

- 什麼是 Python？從計算機談起
- 兩種啟動方式：直譯器 vs Colab/Jupyter
- 基本資料型態：`int`、`str`、`list`、`dict`
- 條件判斷：`if / else`
- 基本迴圈：`for`
- 函式：`def`
- 小結：從互動介面到 `.py` 腳本

---

# 一、什麼是 Python？

## 從計算機談起

::: {style="display: flex; gap: 3rem; align-items: flex-start;"}

::: {style="flex: 1;"}
**傳統計算機**

- 打 `2 + 2`，得到 `4`
- 打 `5 * 5`，得到 `25`
- 輸入指令 → 立即回應
:::

::: {style="flex: 1;"}
**Python 直譯器**

```python
>>> 2 + 2
4
>>> 5 * 5
25
>>> "央行" + "經研處"
'央行經研處'
```
:::

:::

> 本質上是一樣的事情，只是計算機變強了很多。

---

## Python 能做計算機做不到的事

```python
# 把結果存起來
x = 2 + 2

# 處理文字
name = "實價登錄"

# 處理一整批資料
prices = [1500, 2300, 1800, 2100]

# 自動重複執行
for p in prices:
    print(p * 0.9)
```

> 計算機只能算一個數字；Python 可以處理整份資料。

---

# 二、兩種啟動方式

## 方式一：直譯器（終端機）

直接在終端機啟動，逐行執行，即時回應

```bash
# 在終端機輸入
python

# 進入互動介面後
>>> print("Hello, World!")
Hello, World!
>>> 1 + 1
2
```

**特點：**

- 最接近 Python 本質的操作方式
- 適合快速測試單行指令
- 了解直譯器如何「讀一行、跑一行」

---

## 方式二：Colab / Jupyter Lab

在瀏覽器裡執行，以「格子（cell）」為單位

**特點：**

- 畫面友善，適合邊寫邊看結果
- 背後其實是 **IPython**（Python 的強化版互動介面）
- Cell 的概念是 IPython 加上的，不是 Python 原生的

> 注意：Colab/Jupyter 裡有 `%timeit`、`!pip install` 等 `%` 開頭的指令，  
> 那是 IPython 的 magic 指令，**不是標準 Python 語法**。

---

## 兩種方式的關係

```
你在瀏覽器看到的介面（Jupyter / Colab）
            ↓
        IPython Kernel
            ↓
       Python 直譯器  ← 這才是核心
```

**無論哪種方式，最終都是 Python 直譯器在執行你的程式碼。**

> VS Code、PyCharm、Colab——這些工具都只是幫你管理程式碼、  
> 然後呼叫直譯器而已。

---

## 最簡單的方式：Notepad + .py 檔

1. 打開記事本（Notepad）
2. 寫幾行 Python
3. 存成 `hello.py`
4. 在終端機執行

```bash
python hello.py
```

> 語法正確就能跑。不需要任何 IDE、不需要 Colab。  
> **這才是 Python 最純粹的樣子。**

---

# 三、基本資料型態

## 整數與浮點數 `int` / `float`

```python
# 整數
year = 2024
count = 150000

# 浮點數（有小數點）
price = 1580.5
rate = 0.035

# 基本運算
print(price * 1.05)     # 乘
print(count // 1000)    # 整數除法
print(year % 100)       # 取餘數
```

---

## 字串 `str`

```python
city = "台北市"
district = "大安區"

# 合併字串
location = city + district
print(location)          # 台北市大安區

# 取得長度
print(len(city))         # 3

# 切片
print(city[0])           # 台
print(city[:2])          # 台北
```

---

## 串列 `list`

```python
# 儲存一批資料
prices = [1500, 2300, 1800, 2100, 1950]

# 取得單一元素（從 0 開始）
print(prices[0])         # 1500
print(prices[-1])        # 1950（最後一個）

# 新增元素
prices.append(2200)

# 取得長度
print(len(prices))       # 6
```

---

## 字典 `dict`

```python
# 用「鍵值對」儲存資料
record = {
    "縣市": "台北市",
    "鄉鎮市區": "大安區",
    "總價元": 15800000,
    "建物移轉總面積": 45.3
}

# 取得值
print(record["縣市"])           # 台北市
print(record["總價元"])         # 15800000

# 新增欄位
record["單價"] = record["總價元"] / record["建物移轉總面積"]
```

---

# 四、條件判斷

## `if / elif / else`

```python
price = 15800000

if price > 20000000:
    print("高總價物件")
elif price > 10000000:
    print("中總價物件")
else:
    print("低總價物件")
```

輸出：

```
中總價物件
```

> 注意：Python 用**縮排**（4個空格）來表示程式碼的從屬關係，  
> 不是用大括號 `{}`。

---

# 五、基本迴圈

## `for` 迴圈

```python
cities = ["台北市", "新北市", "桃園市", "台中市"]

for city in cities:
    print(city)
```

輸出：

```
台北市
新北市
桃園市
台中市
```

---

## 迴圈 + 條件判斷

```python
records = [
    {"縣市": "台北市", "總價元": 15800000},
    {"縣市": "新北市", "總價元": 8500000},
    {"縣市": "台中市", "總價元": 6200000},
]

for r in records:
    if r["總價元"] > 10000000:
        print(r["縣市"], "：高總價物件")
    else:
        print(r["縣市"], "：一般物件")
```

---

# 六、函式

## 為什麼需要函式？

```python
# 沒有函式：重複寫同樣的邏輯
price1 = 15800000 / 45.3
price2 = 8500000 / 32.1
price3 = 6200000 / 28.7

# 有函式：包起來，重複使用
def 計算單價(總價, 面積):
    return 總價 / 面積

price1 = 計算單價(15800000, 45.3)
price2 = 計算單價(8500000, 32.1)
price3 = 計算單價(6200000, 28.7)
```

> 函式就像計算機上的「自訂按鍵」，你可以自己做一個。

---

## 函式也是變數

```python
def 計算單價(總價, 面積):
    return 總價 / 面積

# 函式本身也是一個變數
print(type(計算單價))
# <class 'function'>

# 可以指派給另一個變數
f = 計算單價
print(f(15800000, 45.3))
```

**普通變數** → 存放數字、字串、串列  
**函式變數** → 存放「可以被呼叫執行的動作」

> 差別只有一個：函式是 **callable**（可呼叫的）。

---

# 七、從互動介面到 .py 腳本

## 把剛才學的全部放進一個檔案

```python
# clean_basic.py

def 計算單價(總價, 面積):
    return round(總價 / 面積, 0)

records = [
    {"縣市": "台北市", "總價元": 15800000, "面積": 45.3},
    {"縣市": "新北市", "總價元": 8500000,  "面積": 32.1},
    {"縣市": "台中市", "總價元": 6200000,  "面積": 28.7},
]

for r in records:
    r["單價"] = 計算單價(r["總價元"], r["面積"])
    print(r["縣市"], "單價：", r["單價"], "元/坪")
```

```bash
python clean_basic.py
```

---

## 本節小結

| 概念 | 對應的計算機概念 |
|:---|:---|
| 直譯器 | 計算機本體 |
| `int` / `float` | 一般數字 |
| `str` | 文字標籤 |
| `list` | 一排按鍵 |
| `dict` | 有標籤的按鍵 |
| `if / for` | 條件與重複操作 |
| `def` | 自訂按鍵（功能鍵）|
| `.py` 檔 | 把一系列按鍵操作存起來 |

---

## 下一節預告

> 現在我們有了基本工具。  
> 接下來要用 **pandas** 一次處理幾萬筆實價登錄資料——  
> 而不是一筆一筆用 `for` 迴圈慢慢跑。

```python
import pandas as pd

df = pd.read_csv("lvr_land_a.csv", skiprows=1)
print(df.shape)      # (87423, 31)
```
