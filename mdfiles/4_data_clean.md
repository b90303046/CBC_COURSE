---
# =========================================
# YAML Front Matter
# ===========================================
title: 運用Python進行資料清理之實務操作： 
subtitle: 資料清理

author: 俞欣榮
date: 2026年7月
institute: 中央銀行經濟研究處
theme: white          # reveal.js 主題：black / white / moon / solarized / sky
slideNumber: true     # 顯示投影片頁碼
transition: slide     # 切換動畫：slide / fade / convex / none
---
 
## 本節課程大綱(資料清理)

1. 補上交易城市別
   - 都會區資料的對應與彙整(mapping)
2. 交易年月日欄位的轉換（`datetime`）
3. 文字處理(`str.contains`):
   - 住宅交易篩選
   - 主要用途篩選
4. 處理數字欄位
   -應用: 每坪單價換算（排除車位價格）


---

## 回顧上一節課程：

之前執行`pd.read_csv`, 受到第一列英文名稱影響，所有資料都自動轉成字串

實價登錄資料中，最常使用的資料欄位有幾個:

1. 交易年月日 
2. 交易標的 (房地、土地、建物、車位)
3. 主要用途 (是否符合央行選擇性信用管制規範"住")
4. 總價元
5. 建物移轉總面積平方公尺


實價登錄並未<span class='highlight'>該筆交易的城市</span>, 需要自己補

---

## 補上城市地區(1)

每一個資料夾中都有一個`manifest.csv`檔案, <span class='highlight'>描述每一個檔案的對應名稱</span>

```python 
# 假設已經設定好manifest路徑
manifest = pd.read_csv('D:/RETR_data/2026q1/manifest.csv', encoding='utf-8')
manifest

                       name                schema  description
0          a_lvr_land_a.csv       schema-main.csv     臺北市不動產買賣
1    a_lvr_land_a_build.csv      schema-build.csv   臺北市建物不動產買賣
2     a_lvr_land_a_land.csv       schema-land.csv   臺北市土地不動產買賣
3     a_lvr_land_a_park.csv       schema-park.csv  臺北市停車場不動產買賣
4          a_lvr_land_b.csv  schema-main-sale.csv     臺北市預售屋買賣
..                      ...                   ...          ...
227  x_lvr_land_c_build.csv      schema-build.csv   澎湖縣建物不動產租賃
228   x_lvr_land_c_land.csv       schema-land.csv   澎湖縣土地不動產租賃
229        z_lvr_land_a.csv       schema-main.csv     連江縣不動產買賣
230  z_lvr_land_a_build.csv      schema-build.csv   連江縣建物不動產買賣
231   z_lvr_land_a_land.csv       schema-land.csv   連江縣土地不動產買賣

```

**要處理的工作**

1. 取出'name'欄位的第一個字母
2. 取出'description'的前三個文字('台北市','新北市',...'連江縣')
3. 只選'name', 'description'兩個欄位
4. 移除重複的資料
5. 轉成dict， 形成"鍵-值"的對應關係
   

---

## 補上城市地區(2)

**DataFrame運算小工具: `apply` + `lambda`**

- 由於 'name', 'description' 都是文字,  可以使用文字的擷取
- `apply` +  `lambda` 是特別設計給`pd.DataFrame`處理簡單運算的函式
   - <span class='highlight'>一般函數亦可應用`apply`來修改資料</span>

```python
manifest['name'] = manifest['name'].apply(lambda x: x[0])
manifest['description'] =manifest['description'].apply(lambda x: x[:3])
```

**排除重複列** : 
- 使用 `df.drop_duplicates()`
- 使用 **dict** 與 list comprehension的方法建構對應關係
  
```python
manifest_map = manifest[['name','description']].drop_duplicates() 
city_map = {letter:city for letter,city in manifest_map.values}
```  

**建立對應關係後**，使用`map`函數置換"城市"欄位:

```python
presale['城市'] = presale['城市'].map(city_map)
```

---

## 都會區資料的對應與彙整(mapping)

運用前述的概念，可以將剛剛的城市資料進行初步<span class='highlight'>"聚合"</span>

1. 保留六都城市名稱
2. 新竹市、新竹縣改為"新竹縣市"
3. 其餘歸類為"其他地區"

初步統計各城市交易:

```python
>>> presale['城市'].value_counts()
城市
新北市    3042
桃園市    2044
.
.
基隆市      20
澎湖縣       1
Name: count, dtype: int64
```

定義以下函式:

```python
def group_region(x:str) -> str:
   metro_6 = ['臺北市','新北市','桃園市','臺中市','臺南市','高雄市']
   hsinchu  = ['新竹市','新竹縣']
   if x in metro_6:
      y =x
   elif x in hsinchu:
      y = '新竹縣市'
   else:
      y = '其他地區'
   return y

presale['都會區'] = presale['城市'].apply(group_region)
```

--- 

## 修正交易年月日格式

在`pandas`中, 時間資料通常應設定為`pd.timestamp`格式, 以方便進行後續分析

- 預售屋交易年月日期格式主要是由民國年月七碼構成
- 需要設計一個函式拆分數字，並且將年加上1911
- 再使用 `pd.to_datetime` 解析文字為日期
  
```python
>>> presale['交易年月日'].head(5)
1     1141111
2     1141113
3     1141114
4     1141114
5     1141116
```

```python
presale['交易年月日']=presale['交易年月日'].apply(lambda x: str(int(x[:3])+1911)+'-'+ x[3:5]+'-'+ x[5:])
presale['交易年月日']=pd.to_datetime(presale['交易年月日'], format = '%Y-%m-%d')
>>> presale['交易年月日'].head()
1   2025-11-11
2   2025-11-13
3   2025-11-14
4   2025-11-14
5   2025-11-16
Name: 交易年月日, dtype: datetime64[us]
```

---

## 文字處理(類別變數)

`DataFrame` 中，部分字串欄位的內容並非自由文字，而是由<span class='highlight'>有限個固定值</span>反覆出現所構成，具有**類別變數（categorical variable）**的性質。

- 比較`土地位置建物門牌`與`交易標的`/`主要用途`的差異
- 針對<span class='highlight'>類別變數</span>，可使用`df.value_counts()`進行初步統計

```python 
>>> presale['交易標的'].value_counts()
交易標的
房地(土地+建物)+車位    888
房地(土地+建物)       285
車位               11
Name: count, dtype: int64

>>> presale['主要用途'].value_counts()
主要用途
住家用        1070
住商用          45
見其他登記事項      43
商業用          17
工業用           6
停車空間          3
Name: count, dtype: int64
```

<span class='highlight'>`df.value_counts()`可以初步針對"類別變數"進行初步統計</span>

---

## 文字處理(類別變數)的篩選

在進行不動產交易資料分析中，主要關注以下交易：
1. 交易標的：房地(土地+建物)+車位、 房地(土地+建物)
2. 主要用途：與住相關的交易(住家用、住商用)

&rarr; <span class='highlight'>使用`str.contains()`指令 </span> 

```python
# 搜尋包含有"房地"的關鍵字, 輸出為Boolean值
bool_house_land = presale['交易標的'].str.contains('房地', na=False) #如果沒資料, 視為否

# 搜尋主要用途
live_pattern = '|'.join(['住家用','住商用']) # 建立聯集字串
bool_live = presale['主要用途'].str.contains(live_pattern,na=False)


# copy() 避免警告, 因為資料清理過程有刪除部分列資料
presale_clean = presale.copy()[bool_live & bool_house_land] #兩者取交集

```

檢查篩選後的`presale_clean`結果:

```python
>>> presale_clean['主要用途'].value_counts()
主要用途
住家用    1062
住商用      45
Name: count, dtype: int64
>>> presale_clean['交易標的'].value_counts()
交易標的
房地(土地+建物)+車位    838
房地(土地+建物)       269
Name: count, dtype: int64
```

---

## 處理數字欄位(1)

實價登錄資料中，重要的數字欄位資料如下：
1. 總價元、 車位總價元、
2. 建物移轉總面積平方公尺、車位移轉總面積平方公尺

本節任務:
   1. 將資料轉為數字欄位(目前為文字)
   2. 將總價元轉為萬元單位;  平方公尺轉為坪
   3. 在排除車位面積與車位價格後，計算每坪單價

**轉換數字功能**: `pd.to_numeric`，並強制將有問題的資料強制轉為NaN

```python
# 定義num_cols list
num_cols = ['總價元','車位總價元','建物移轉總面積平方公尺','車位移轉總面積平方公尺']

for col in num_cols:
   presale_clean[col]  = pd.to_numeric(presale_clean[col], errors='coerce')

presale_clean.info()
```

---

## 處理數字欄位(2)：排除車位

計算不含停車位的每坪面積，公式如下：

- 成交價格：如果車位價格大於等於0，則扣除車位價格：若車位價格無資料，則維持原總價格
- 成交面積：如果車位ａ面積大於等於0，則扣除車位面積：若車位面積無資料，則維持原面積
- 使用套件`numpy` 中的`np.where`設計以下條件(參考<a href='https://numpy.org/doc/stable/reference/generated/numpy.where.html'>連結</a>)


```python
# 有車位價格就扣掉，沒有就用原始總價
net_price = ( np.where(
    presale_clean['車位總價元'].notna(),
    presale_clean['總價元'] - presale_clean['車位總價元'],
    presale_clean['總價元']
)/10000)

# 同樣處理面積
net_area = (np.where(
    presale_clean['車位移轉總面積平方公尺'].notna(),
    presale_clean['建物移轉總面積平方公尺'] - presale_clean['車位移轉總面積平方公尺'],
    presale_clean['建物移轉總面積平方公尺'])/3.305785  )  # 換算每坪（1坪 = 3.305785平方公尺）

presale_clean.loc[:,'每坪單價_萬'] = net_price / net_area  #新增欄位

```

---

## 清理後結果彙整

```python
<class 'pandas.core.frame.DataFrame'>
Index: 9679 entries, 0 to 10869
Data columns (total 34 columns):
 #   Column       Non-Null Count  Dtype
---  ------       --------------  -----
 0   鄉鎮市區         9679 non-null   object
 1   交易標的         9679 non-null   object
...
 7   交易年月日        9679 non-null   datetime64[ns]
...
 12  主要用途         9679 non-null   object
...
 21  總價元          9679 non-null   int64
 24  車位移轉總面積平方公尺  9679 non-null   float64
 25  車位總價元        9679 non-null   int64
...
 31  城市           9679 non-null   object
 32  都會區          9679 non-null   object
 33  每坪單價_萬         9679 non-null   float64
dtypes: datetime64[ns](1), float64(3), int64(2), object(28)
memory usage: 2.6+ MB
```

---

## 本節課程快速回顧


| 工具 | 用途 |
|:---|:---|
| `apply` + `lambda` | 逐列文字處理 |
| `dict` comprehension | 建立 key-value 對應表 |
| `str.contains()` | 類別變數篩選 |
| `pd.to_datetime()` | 時間格式轉換 |
| `pd.to_numeric()` | 數字欄位轉換 |
| `np.where()` | 條件式數值運算 |

  
---

## 附錄(VBA計算每坪單價)

```VBA
Sub CalcPricePerPing()
    Dim ws As Worksheet
    Dim i As Long
    Dim lastRow As Long
    Dim netPrice As Double
    Dim netArea As Double
    
    Set ws = ActiveSheet
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    For i = 2 To lastRow
        ' 排除車位價格
        If Not IsEmpty(ws.Cells(i, 25).Value) Then
            netPrice = (ws.Cells(i, 21).Value - ws.Cells(i, 25).Value) / 10000
        Else
            netPrice = ws.Cells(i, 21).Value / 10000
        End If
        
        ' 排除車位面積，換算坪數
        If Not IsEmpty(ws.Cells(i, 24).Value) Then
            netArea = (ws.Cells(i, 15).Value - ws.Cells(i, 24).Value) / 3.305785
        Else
            netArea = ws.Cells(i, 15).Value / 3.305785
        End If
        
        ' 計算每坪單價
        ws.Cells(i, 34).Value = netPrice / netArea
    Next i
End Sub
```

VBA的麻煩之處:

1. 用欄位編號（第21欄、第24欄）而不是欄位名稱，維護時很難對應
2. 逐列跑迴圈，資料量大的時候速度很慢
3. 邏輯分散在多個 If 裡，不容易一眼看懂

---