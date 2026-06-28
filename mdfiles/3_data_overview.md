---
# =========================================
# YAML Front Matter
# ===========================================
title: 運用Python進行資料清理之實務操作： 
subtitle: 資料讀取與合併

author: 俞欣榮
date: 2026年7月
institute: 中央銀行經濟研究處
theme: white          # reveal.js 主題：black / white / moon / solarized / sky
slideNumber: true     # 顯示投影片頁碼
transition: slide     # 切換動畫：slide / fade / convex / none
---
 

## 本節課程大綱：資料讀取與合併

1. 列出資料夾的檔案（`pathlib.Path`）
2. 檔案讀取套件：`pandas`
   - 基本 pandas 介紹
   - 資料讀取（`pd.read_csv`）
   - DataFrame 的三個組成：index、columns、values
   - 資料初步概觀（`df.info`、`df.describe`）
3. 資料合併（`pd.concat`）
4. 綜合應用：合併各類預售屋資料

---

## 列出資料夾的檔案: `pathlib.Path`

在讀取資料之前，第一步是**確認資料夾裡有什麼**

1. 載入模組: 兩種寫法
```python
import pathlib            # 載入整個模組
pathlib.Path("data/")     # 要加模組名稱才能使用

from pathlib import Path  # 只載入 Path 類別
Path("data/")             # 可以直接用，不用加前綴
```

2. 指定資料夾路徑

```python
data_dir = Path("D:/data/") #絕對或相對路徑皆可

pwd = Path.cwd()  # 列出目前的檔案路徑
```

---


## 列出檔案並篩選

用 `glob` 篩選特定特定符合字元的檔案

```python 
from pprint import pprint  #漂亮列印
# 只列出 CSV 檔案, 並轉換成list
csv_files = list(data_dir.glob("*.csv"))
pprint(csv_files)

# 預售屋資料通常以特定字元開頭，例如 lvr_land_b
presale_files = list(data_dir.glob("*_b.csv"))
print(presale_files)
```

**`glob` 的 `*` 是萬用字元，代表任意字串**

*其他指令*

- 找出母資料夾: `file.parent`
- 檔案名稱: `file.stem` / `file.name` (含副檔名)
- 檢查是檔案/資料夾: `Path.is_file`/`Path.is_dir()`


---

## 什麼是 pandas？

- Python 中最常用的**資料處理**套件
- 核心物件：**DataFrame**（類似 Excel 的二維表格）
- 匯入慣例：
  1. 使用前先安裝
   
     ```powershell
     # 如果僅安裝miniconda
     pip install pandas 
     conda install -c conda-forge pandas
     ```

  2. 載入模組
   
    ```python
    import pandas as pd
    print(pd.__version__)  # 查詢版本
    ```

  3. 讀取資料(2026Q1,台北市預售屋資料): <a href='https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html'>`pd.read_csv`</a>
   
    ```python
    df = pd.read_csv(presale_files[0], encoding="utf-8",  on_bad_lines='skip') 
    ```
    - `encoding`:  使用utf-8編碼
    - `on_bad_lines`: 跳過讀取有錯誤的資料

---

## `pd.read_csv`：讀取 CSV 檔案的編碼設定(encoding)


|編碼參數|定義|
|:---:|:---:|
|`utf-8`| 萬國碼(預設) |
|`cp950`|繁體中文 Windows|
|`utf-8-sig`|含 BOM 的 UTF-8|

- 內政部實價登錄資料早期多為 `cp950`，近年逐漸改為 `utf-8`  
- 遇到 `UnicodeDecodeError` 時，先試<span class='highlight'> `cp950`</span>
- 匯入成功, 先看前幾筆(預設5筆)資料

  ```python
    df.head()
  ```

  <span class='highlight'>發現第二列資料是英文的欄位名稱</span>


---

## DataFrame 的三個組成

DataFrame 由三個部分構成：

```python
df.index    # 列索引（row labels）
df.columns  # 欄名稱（column labels）
df.values   # 實際資料（numpy array）
 
# 列索引：預設是 0, 1, 2, 3...
print(df.index)
# RangeIndex(start=0, stop=1000, step=1)

# 欄名稱：資料的每個變數
print(df.columns)
# Index(['鄉鎮市區', '交易標的', '土地位置建物門牌', '交易年月日', '總價元'], dtype='object')

# 實際資料：純數值陣列（numpy array）
print(df.values)
```

- `df.values` 是 numpy array，這也是 pandas 底層的儲存結構<br>
- 發現第一列是英文欄位, 進行資料切片, 依據index位置**切片**<span class='highlight'>從第1個index開始算</span>:
  
  ```python
  df = df.iloc[1:,:]  #從第2列資料開始讀取
  ```
---

## `df.info()`：資料初步檢查

```python
df.info()
```

```python
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1185 entries, 0 to 1184
Data columns (total 31 columns):
 #   Column    Non-Null Count  Dtype
---  ------    --------------  -----
 0   鄉鎮市區         1185 non-null   str
 1   交易標的         1185 non-null   str
 2   土地位置建物門牌     1185 non-null   str
 3   土地移轉總面積平方公尺  1185 non-null   str
 .
 .
 .
 23  車位類別         893 non-null    str
 24  車位移轉總面積平方公尺  1185 non-null   str
 25  車位總價元        1185 non-null   str
 26  備註           182 non-null    str
 27  編號           1185 non-null   str
 28  建案名稱         1185 non-null   str
 29  棟及號          1185 non-null   str
 30  解約情形         2 non-null      str

dtypes: str(31)
memory usage: 613.9 KB

```
重點看：
- Dtype : 每個欄位的資料型態
- **Non-Null Count**：有沒有缺漏值（`2 non-null` 只有兩筆有註記解約）

---


## 資料合併: `pd.concat`：垂直堆疊多個 DataFrame

- 實價登錄資料通常**每個縣市一個檔案(a: 台北市, b:台中市...)**，需要<span class='highlight'>合併成一張大表</span>
1. 先前已整理`presale_files`，列出各縣市的實價登錄資料
2. 寫一個 `for`迴圈， 搭配`pd.read_csv`， 讀取所有的資料
3. 運用`pd.concat`合併所有下載完的資料

```python
# 逐一讀取並合併
df_list = []
for f in presale_files:
    city = f.stem[0] # 取出第一個字碼, 等等轉為城市
    df_temp = pd.read_csv(f, encoding="utf-8", on_bad_lines='skip')
    df_temp['城市'] = city   # 新增一個城市欄位
    df_list.append(df_temp)

presale = pd.concat(df_list, join='outer', axis=0, ignore_index=True)
print(presale.shape)
```
---

## `pd.concat`參數說明

1. `axis=0`: 決定垂直合併還是水平合併
2. `join="outer"`: 包含沒有交集的欄位, `inner`是僅保留交集的欄位
3. `ignore_index=True`：重設列索引


<span class ='highlight'>不加 `ignore_index=True` 會導致後續 `df.loc[0]` 取到多筆，  是初學者很常遇到的 bug</span>


合併後記得確認結果

```python
# 合併後的基本確認
print(presale.shape)   # (總筆數, 欄數)
presale.info()         # 有無缺漏值、型態是否正確
presale.head()         # 目測前幾筆是否正常
```
 
---

## 本節小結

| 工具 | 用途 |
|:---|:---|
| `pathlib.Path.glob()` | 批次找出目標檔案 |
| `pd.read_csv()` | 讀取 CSV，注意編碼 |
| `df.index` / `.columns` / `.values` | DataFrame 的三個組成 |
| `df.info()` | 確認缺漏值與資料型態 |
| `pd.concat(..., ignore_index=True)` | 合併多個 DataFrame，避免 index 重複 |

<span class='highlight'>**建議：** 每次讀完資料，先跑 `info()`, 確認資料品質後再做後續清理與分析</span>

