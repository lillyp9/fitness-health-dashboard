import pandas as pd 
import sqlite3


#connet with database
conn = sqlite3.connect("../data/fitness.db")
#What is the total volume per exercise 
query = """

SELECT exercise ,SUM(volume) AS exercise_volume_total
FROM lifting
GROUP BY exercise 
ORDER BY exercise_volume_total DESC
"""

result = pd.read_sql_query(query, conn)
print(result)
#what is the weekly progression per exercise 
query2 = """
SELECT exercise , AVG(weight_lbs) AS avg_weight , AVG(reps) AS avg_reps
FROM lifting
GROUP BY exercise , date 
ORDER BY exercise, date DESC
"""
result2 = pd.read_sql_query(query2, conn)
print(result2)

#What is the metrics by day of week 
query3 = """
SELECT day_of_week , AVG(steps) AS avg_steps, AVG(sleep_hours) AS avg_sleep, AVG(resting_heart_rate) AS avg_rhr
FROM health 
GROUP BY day_of_week
ORDER BY avg_steps DESC
"""
result3 = pd.read_sql_query(query3, conn)
print(result3)

#Which muscle group generate the most average volume per set and  which muscle group has the highest average reps per set?
query4 = """
SELECT muscle_group ,AVG(reps) AS avg_reps, AVG(volume) AS avg_volume 
FROM lifting 
GROUP BY muscle_group
ORDER BY avg_volume , avg_reps DESC
"""

result4 = pd.read_sql_query(query4,conn)
print(result4)
