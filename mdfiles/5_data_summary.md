---
# =========================================
# YAML Front Matter
# ===========================================
title: 運用Python進行資料清理之實務操作： 
subtitle: 基本統計分析

author: 俞欣榮
date: 2026年7月
institute: 中央銀行經濟研究處
theme: white          # reveal.js 主題：black / white / moon / solarized / sky
slideNumber: true     # 顯示投影片頁碼
transition: slide     # 切換動畫：slide / fade / convex / none
---
 
## 本節課程大綱(基本統計分析)

1. 調整交易年月日格式
2. 資料聚合
   - 基本概念與指令
   - 資料聚合應用: 計算交易量、每坪單價中位數
3. 資料匯出（`to_csv`、`to_excel`）

---

## 調整交易年月日格式(交易年月統一化)

觀察傳統的內政統計月報、物價統計月報、大多是以<span class='highlight'>年-月</span>進行統計

- 檢視實價登錄資料:

   ```python
   >>> presale_clean['交易年月日'].head()
   0   2025-11-11 
   1   2025-11-13
   2   2025-11-14
   3   2025-11-14
   4   2025-11-16
   Name: 交易年月日, dtype: datetime64[ns]
   ```
   是以年-月-日進行統計

- 使用`.dt.to_period('M')`, `.dt.to_period('Q')`, `.dt.to_period('Y')`, 分別註記每一筆交易究竟是落在哪一個<span class='highlight'>交易月、交易季、交易年</span>的時間區段內

```python
presale_clean['交易月'] = presale_clean['交易年月日'].dt.to_period('M') 
presale_clean['交易季'] = presale_clean['交易年月日'].dt.to_period('Q') 
presale_clean['交易年'] = presale_clean['交易年月日'].dt.to_period('Y') 
```

---

## `groupby` 的概念

`groupby` 的邏輯類似 Excel 的<span class='highlight'>樞紐分析表</span>：指定分組依據，對每個組合套用統計函數

```python
# 基本結構
df.groupby(['欄位A', '欄位B']).統計函數()

# 常用統計函數
.size()      # 計算筆數（交易量）
.median()    # 中位數
.mean()      # 平均數
.sum()       # 加總
```

| 參數 | 說明 |
|:---|:---|
| `observed=False` | 沒有資料的組合也列出（值為 0 或 NaN） |
| `.unstack('欄位')` | 將指定的 index 轉成欄位，方便閱讀 |

<span class='highlight'>**`groupby` 後，分組欄位會自動變成 DataFrame 的 index**</span>

---

## 資料聚合統計(1)：計算交易量

藉由標註交易時間的區段、搭配都會區的註記資料，進行以下計算：

1. 給定特定「交易月」、「都會區」，彙整成交案件數量
2. 給定特定「交易月」、「都會區」，計算總價元的中位數
3. 給定特定「交易月」、「都會區」，計算每坪單價的中位數

&rarr; 使用`df.groupby(['交易月','都會區'], observed=False)` 進行資料聚合
 
```python
region_order = ['全國', '臺北市', '新北市', '桃園市', '臺中市', '臺南市', '高雄市']

# 將具有相同交易月、都會區的資料進行彙整
# 此時交易月、都會區將轉成 DataFrame 的 index
presale_transaction = presale_clean.groupby(['交易月','都會區'], observed=False).size()
presale_transaction = presale_transaction.unstack('都會區')

# 將統計的結果進行橫向相加，得到全國資料
presale_transaction['全國'] = presale_transaction.sum(axis=1)

# 重新排序欄位
presale_transaction = presale_transaction[region_order]
```

---

## 資料聚合統計(2)：計算總價中位數

運用相同方法可以計算成交總價的中位數：

```python
# 各都會區中位數
presale_total_price = (
    presale_clean
    .groupby(['交易月','都會區'], observed=False)['總價元']
    .median()
    .unstack('都會區')
    / 10000
)

# 全國中位數（不分都會區）
presale_total_price_all = (
    presale_clean.groupby(['交易月'], observed=False)['總價元'].median() / 10000
)
presale_total_price_all.name = '全國'

# 合併全國與各都會區，並重新排序
presale_total_price = (
    pd.concat([presale_total_price_all, presale_total_price], axis=1, join='outer')
    [region_order]
)
```

- 同樣方法亦可應用在「每坪單價」的統計上

---

## 資料匯出

```python
# 匯出 CSV（建議用 utf-8-sig，Windows Excel 開啟才不會亂碼）
presale_transaction.to_csv('output/transaction.csv', encoding='utf-8-sig')
presale_total_price.to_csv('output/total_price.csv', encoding='utf-8-sig')
```

```python
# 匯出 Excel（多個 DataFrame 寫入同一檔案的不同工作表）
with pd.ExcelWriter('output/presale_summary.xlsx') as writer:
    presale_transaction.to_excel(writer, sheet_name='交易量')
    presale_total_price.to_excel(writer, sheet_name='總價中位數')
```

| 格式 | 優點 | 注意事項 |
|:---|:---|:---|
| `to_csv` | 輕量、通用 | encoding 用 `utf-8-sig` |
| `to_excel` | 可多工作表 | 需安裝 `openpyxl` |

(`pip install openpyxl`)

---

## 本節課程快速回顧

| 工具 | 用途 |
|:---|:---|
| `.dt.to_period()` | 時間資料轉換為年月季年區段 |
| `groupby()` | 依指定欄位分組聚合（類似樞紐分析表） |
| `.size()` | 計算各組筆數 |
| `.median()` | 計算各組中位數 |
| `.unstack()` | 將 index 轉為欄位，方便閱讀 |
| `to_csv()` | 匯出 CSV，注意 encoding |
| `to_excel()` | 匯出 Excel，可多工作表 |

---
