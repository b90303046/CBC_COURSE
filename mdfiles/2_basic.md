---
# =========================================
# YAML Front Matter
# ===========================================
title: 運用Python進行資料清理之實務操作： 
subtitle: 基本Python介紹

author: 俞欣榮
date: 2026年7月
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

- Python中，每一個變數都有屬於自己的<span class="highlight">型態</span>，各種型態的屬性也不同
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
| `dict` | 鍵值對應 | `{"縣市": "台北市","總價": 1500}`| 一列資料(有欄位) |


**補充**

- 上述的變數型態，是資料內最常見的組成(大家可以回想Excel表)
- 在python的環境中, Excel表是以<span class="highlight">`pandas.DataFrame`呈現</span>


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
- list：可以裝不同型態
- Python 的第一個數字是從`0`開始 

```python
prices = [1500, 2300, 1800, 2100, 'a','b','c'] #7個元素

# 取值：從 0 開始數（不是從 1）
prices[0]    # 1500  ← 第一個
prices[-1]   # 'c'  ← 最後一個

# 切片
prices[1:3]  # [2300, 1800]
# 新增
prices.append(1950)
# 長度
len(prices)  # 8
# 巢狀list 
table = [
    ["台北市", 7000],
    ["新北市", 6000],
    ["其他", 4000]
]
```


 

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


## 函式

- 函式也是變數的一種
    - **普通變數** → 存放數字、字串、串列  
    - **函式變數** → 存放「可以被呼叫執行的動作」
> 差別只有一個：函式是 **callable**（可呼叫的）。

- 函式的用途：**自行設計一個類似計算機上可重複使用的「自訂按鍵」**

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


## 函式的型別提示（Type Hint）

設計函式時，**建議對輸入與輸出進行型別提示**

```python
# 沒有type hint：不知道要傳入什麼、會回傳什麼
def 計算單價(總價, 面積):
    return 總價 / 面積

# 有type hint：清楚標示輸入與輸出的型態
def 計算單價(總價: int|float, 面積: float) -> float:
    return 總價 / 面積
```

**讀法：**

- `總價: int` → 這個參數應該傳入整數
- `面積: float` → 這個參數應該傳入浮點數
- `-> float` → 這個函式會回傳浮點數

> 類似Excel裡設定「這格是數字、那格是文字」——  
> type hint讓你跟別人都清楚這個函式在處理什麼型態的資料。


## `for` 迴圈

`for` 迴圈：對一批資料**逐一處理**，不用重複寫相同的程式碼。

- 案例1: 假設我有一串價格資料，印出每筆打9折的價格
```python
prices = [1500, 2300, 1800, 2100]

for p in prices:     # p即是迭代prices裡面的元素
    print(p * 0.9)   # 每筆打九折
```

- 案例2： 搭配 `range()`
   - **注意：`range()` 不會直接顯示數字**

```python
# range(5) 產生產生 0, 1, 2, 3, 4
result = [i**2 for i in range(5)] # 簡潔寫法(list comprehension), 產生0, 1, 4, 9, 16 
```

- 案例3: 在`dict`執行`for`迴圈

```python
record = {
    "縣市":  "台北市",
    "總價":  1500,
    "坪數":  32.5
}
# 同時取 key 和 value
for key, value in record.items():
    print(key, "→", value)
```


## `if` 條件判斷與Boolean值

Python 可以看段一段敘述的真與偽, 並將結果輸出為Boolean值(另一個Python變數型態)

```python
price = 4500

bool1, bool2, bool3 = price>4000,  price == 4000, price < 4000
if bool1:
    print("高於門檻")
elif bool2:
    print("剛好等於門檻")
else:
    print("低於門檻")
```

**for迴圈與if條件式的縮排規則**

Python 用**縮排**決定程式碼的層級
    - 同一個縮排位置代表在同一個迴圈內執行

```python
for p in prices:
    if p > 2000:
        print(p)
print('執行結束')  # 因為和for同一層級，只會印一次
```


## 綜合應用 : list of dict
考慮以下隨機從實價登錄抓出來的部分資料
  - 資料外層是list, 每一個list的元素是dict
  - 每一個dict的鍵(key)是交易資訊(交易年月日、城市、...):

```python
sample =[
 {'交易年月日': '2023-04-20','城市': '桃園市','建案名稱': '僑駿LIFE 耘邸','總價萬': 1440.0,'鄉鎮市區': '蘆竹區'},
 {'交易年月日': '2024-07-13','城市': '新北市','建案名稱': '立信雙星','總價萬': 2231.0,'鄉鎮市區': '板橋區'},
 {'交易年月日': '2022-03-29','城市': '桃園市','建案名稱': '華曜大謙','總價萬': 1248.0,'鄉鎮市區': '龍潭區'},
 {'交易年月日': '2021-11-18','城市': '桃園市','建案名稱': '福鄉至美','總價萬': 1300.0,'鄉鎮市區': '桃園區'},
 {'交易年月日': '2023-04-06','城市': '高雄市','建案名稱': '宏道文華帝寶','總價萬': 1253.0,'鄉鎮市區': '三民區'},
 {'交易年月日': '2021-11-06','城市': '新北市','建案名稱': '馥華城奕','總價萬': 3799.0,'鄉鎮市區': '土城區'},
 {'交易年月日': '2023-03-19','城市': '桃園市','建案名稱': '新潤麗蒔','總價萬': 953.0,'鄉鎮市區': '蘆竹區'},
 {'交易年月日': '2022-05-28','城市': '高雄市','建案名稱': '艾美MOMA2','總價萬': 1222.0,'鄉鎮市區': '小港區'},
 {'交易年月日': '2024-08-31','城市': '彰化縣','建案名稱': '飛夢市','總價萬': 1268.0,'鄉鎮市區': '埔心鄉'},
 {'交易年月日': '2022-11-04','城市': '臺中市','建案名稱': '昌祐蒔上','總價萬': 1455.0,'鄉鎮市區': '北屯區'}
 ]
```

**應用**: 找出總價超過**1500萬**的交易，並印出城市、建案名稱與總價 

```python
for record in sample:
    if record["總價萬"] > 1500:
        print(record["城市"], record["建案名稱"], record["總價萬"])
```











