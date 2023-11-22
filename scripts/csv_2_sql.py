import pandas as pd

# 读取CSV文件
df = pd.read_csv("data/drugs.csv")

import sqlite3

# 创建或连接到SQLite数据库
conn = sqlite3.connect("data/drugs.db")

# 将数据导入到新表中
df.to_sql("drug_info", conn, if_exists="replace", index=False)
