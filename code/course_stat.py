import pandas as pd

sht_name = "經濟研究處訓練課程運用Python進行資明細表"

old_col = ['填答人員', '經濟研究處訓練課程-「運用Python進行資料清理之實務操作：內政部不動產交易實價登錄資料之建構、清理與分析」參加人員調查']
new_col = ['name', 'status']

pattern_name = r'(.+)\('
df = (pd.read_excel(r'../course_member.xlsx', sheet_name=sht_name, skiprows=2)
      .rename(columns = dict(zip(old_col, new_col)))
      .assign( name = lambda df: df['name'].str.extract(pattern_name, expand=False))
      .query('status =="參加實體"')
      )

all_members = ';'.join(df['name'].to_list())

with open(r'../file.txt', 'w') as ww:
    ww.writelines(all_members)