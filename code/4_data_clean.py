# 延續前一節的結果
from pathlib import Path
import pandas as pd
from pprint import pprint

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




dir_loc = Path("D:/RETR_data/2026q1")

presale_files = [jj for jj in dir_loc.glob('*_b.csv')]


df_list = []
for f in presale_files:
    city = f.stem[0] # 取出第一個字碼, 等等轉為城市
    df_temp = pd.read_csv(f, encoding="utf-8", on_bad_lines='skip').iloc[1:,:]
    df_temp['城市'] = city   # 新增一個城市欄位
    df_list.append(df_temp)

presale = pd.concat(df_list, join='outer', axis=0, ignore_index=True)


# 第三節課程開始

# 處理城市資料
manifest = pd.read_csv('D:/RETR_data/2026q1/manifest.csv', encoding='utf-8')
manifest['name'] = manifest['name'].apply(lambda x: x[0])
manifest['description'] =manifest['description'].apply(lambda x: x[:3])
manifest_map = manifest[['name','description']].drop_duplicates() 
city_map = {letter:city for letter,city in manifest_map.values}

presale['城市'] = presale['城市'].map(city_map)
presale['都會區'] = presale['城市'].apply(group_region)


# 處理交易年月日
presale['交易年月日']=presale['交易年月日'].apply(lambda x: str(int(x[:3])+1911)+'-'+ x[3:]   )
presale['交易年月日']=pd.to_datetime(presale['交易年月日'], format = '%Y-%m%d')


# 篩選交易標的, 主要用途
# 搜尋包含有"房地"的關鍵字, 輸出為Boolean值
bool_house_land = presale['交易標的'].str.contains('房地', na=False) #如果沒資料, 視為否

# 搜尋主要用途
live_pattern = '|'.join(['住家用','住商用']) # 建立聯集字串
bool_live = presale['主要用途'].str.contains(live_pattern,na=False)

presale_clean = presale.copy()[bool_live & bool_house_land] #兩者取交集


## 處理數值欄位資料
num_cols = ['總價元','車位總價元','建物移轉總面積平方公尺','車位移轉總面積平方公尺']

for col in num_cols:
   presale_clean[col]  = pd.to_numeric(presale_clean[col], errors='coerce')





# 處理面積與總價

# 有車位價格就扣掉，沒有就用原始總價
net_price = np.where(
    presale_clean['車位總價元'].notna(),
    presale_clean['總價元'] - presale_clean['車位總價元'],
    presale_clean['總價元']
)

# 同樣處理面積
net_area = np.where(
    presale_clean['車位移轉總面積平方公尺'].notna(),
    presale_clean['建物移轉總面積平方公尺'] - presale_clean['車位移轉總面積平方公尺'],
    presale_clean['建物移轉總面積平方公尺']
)

# 換算每坪（1坪 = 3.305785平方公尺）
presale_clean['每坪單價_萬'] = net_price / net_area * 3.305785
print('\n ============ \n')
print('第四節資料清理結果如下:')
print(presale_clean.info())