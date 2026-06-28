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
 
## 本節課程大綱(資料讀取與合併)

1. 補上交易城市別
2. 交易年月日欄位的轉換（`datetime`）
3. 文字處理(`str.contains`):
   - 住宅交易篩選
   - 主要用途篩選
4. 都會區資料的對應與彙整(mapping)
5. 聚合（六都 vs 非六都，`str.contains` + `apply`）
6. 每坪單價換算（排除車位價格，`np.where`, 看時間長度）


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
manifest = pd.read_csv('data/manifest.csv', encoding='utf-8')
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
presale['交易年月日']=presale['交易年月日'].apply(lambda x: str(int(x[:3])+1911)+'-'+ x[3:]   )
presale['交易年月日']=pd.to_datetime(presale['交易年月日'], format = '%Y-%m%d')
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

<span class='highlight'>`df.value_counts()`可以初步針對類別變數進行初步統計</span>

---

## 文字處理(類別變數)的篩選

運用


