from pathlib import Path
import pandas as pd
from pprint import pprint

dir_loc = Path("D:/RETR_data/2026q1")

presale_files = [jj for jj in dir_loc.glob('*_b.csv')]


df_list = []
for f in presale_files:
    city = f.stem[0] # 取出第一個字碼, 等等轉為城市
    df_temp = pd.read_csv(f, encoding="utf-8", on_bad_lines='skip').iloc[1:,:]
    df_temp['城市'] = city   # 新增一個城市欄位
    df_list.append(df_temp)

presale = pd.concat(df_list, join='outer', axis=0, ignore_index=True)




 