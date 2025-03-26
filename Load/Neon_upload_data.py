import pandas as pd
from sqlalchemy import create_engine

# 讀取你的CSV資料
df = pd.read_csv("Leetcode 各題目基本資料表 20210712.csv")

user_name = ""
password = ""

# Neon 提供的資料庫連線字串
DATABASE_URL = f"postgresql://{user_name}:{password}@ep-rapid-recipe-a1d6k3o2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# 上傳CSV到Neon PostgreSQL
engine = create_engine(DATABASE_URL)
df.to_sql("mydata", engine, if_exists="replace", index=False)
