import pandas as pd 
import sqlite3

lifting_data = pd.read_csv("../data/lifting_data.csv")
health_data = pd.read_csv("../data/daily_health_metrics.csv")

conn = sqlite3.connect("../data/fitness.db")

#.to_sql() - built in method that takes 3 Arugments ("table-name") , ("conn"), ("if_exists")
#If- exist - have two options ("fail", "replace", "append")- in this case replace 
lifting_data.to_sql("lifting", conn, if_exists="replace", index=False)

health_data.to_sql("health", conn, if_exists="replace", index=False)

print("lifting table saved to database")
print("health table saved to database")

conn.close()