import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
font_setup = {'size':20, 'family':'DFKai-SB3'}
mpl.rc('font',**font_setup)
mpl.rc('axes', unicode_minus=False)

item_name = ["房屋及營建工程","運輸工具","機械設備", "金融性資產淨值",
             "其他","土地"]

item_percent=[17.71, 2.16, 11.31,15.43, 
              7.29, 40.63]







index_order = item_name


color_map = {
    "房屋及營建工程":   '#6EC6C6',
    "運輸工具":        '#D4C84A',
    "機械設備":        '#A0A0A0', 
    "土地":           '#A080C0', 
    "其他": '#E05050',
    "金融性資產淨值":   '#70B050',
}


df = (pd.DataFrame(data = zip(item_name, item_percent), columns=['項目','百分比'])
     .set_index('項目').loc[index_order,:]
     #.reindex(index_order, axis=0)
     )
 

"""
2024年底國富毛額為330.11兆元
"""

# 所有資料從 df 取，不再用原本的 list
colors      = [color_map[name] for name in df.index]
names       = list(df.index)
percents    = list(df['百分比'])

fig, ax = plt.subplots(figsize=(10/1.5, 8/1.5))


wedges, _ = ax.pie(
    percents,
    labels=None,
    colors=colors,
    startangle=135,
    counterclock=False,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=1.5),
)

# 扇形內百分比
for wedge, pct in zip(wedges, percents):
    if pct < 0.5:
        continue
    angle = (wedge.theta1 + wedge.theta2) / 2
    x = 0.75 * np.cos(np.radians(angle))
    y = 0.75 * np.sin(np.radians(angle))
    ax.text(x, y, f'{pct:.2f}%', ha='center', va='center',
            fontsize=11, color='black', fontweight='bold')

# 外部標籤加引線
for wedge, name, pct in zip(wedges, names, percents):
    angle = (wedge.theta1 + wedge.theta2) / 2
    x_inner = 1.05 * np.cos(np.radians(angle))
    y_inner = 1.05 * np.sin(np.radians(angle))
    x_text = 1.30 * np.cos(np.radians(angle))
    y_text = 1.30 * np.sin(np.radians(angle))
    ha = 'center' if abs(x_text) < 0.1 else ('left' if x_text > 0 else 'right')
    ax.annotate(
        name,
        xy=(x_inner, y_inner),
        xytext=(x_text, y_text),
        ha=ha, va='center',
        fontsize=10,
        arrowprops=dict(arrowstyle='-', color='black', lw=0.8),
    )

ax.set_title('2023國富毛額占比:按資產大類分', fontsize=16, pad=20)

loc = Path(__file__).parent.parent /'mdfiles'
fig_loc = loc /'fig1.svg'
fig.savefig(fig_loc, dpi=300, bbox_inches='tight')
 
#plt.show()

print('檔案匯出成功!')