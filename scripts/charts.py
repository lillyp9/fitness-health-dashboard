import pandas as pd 
import sqlite3
import plotly.express as px
import matplotlib.pyplot as plt 

#connect database
conn = sqlite3.connect("../data/fitness.db")
#SQL QUERY 1 total volume by exercise
query = """
SELECT exercise, SUM(volume) AS total_volume
FROM lifting
GROUP BY exercise
ORDER BY total_volume DESC
"""
#print out table 
volume_df = pd.read_sql_query(query, conn)
print(volume_df)

#SQL Query2 - weekly progression
query2 = """
SELECT exercise, date, AVG(weight_lbs) as avg_weight
FROM lifting
GROUP BY exercise, date
ORDER BY exercise, date
"""
#print out table 
progression_df = pd.read_sql_query(query2, conn)
print(progression_df)

#horizontal  chart
fig1 = px.bar( #create bar chart
    volume_df, #dataframe 
    x = "total_volume", # column
    y = "exercise", #column
    orientation = "h", #horizontal 
    title = "Total Volume by Exercise", 
    labels = {"total_volume": "Total volume(lbs x reps)", "exercise": "Exercise"},
    color = "total_volume", #automatic color bars by value , darker = higher
    
)
fig1.show()

#chart2 line chart

fig2 = px.line(
    progression_df,
    x = "date",
    y = "avg_weight",
    color = "exercise",
    title = "Average Weight By Exercise Over Time",
) 
fig2.show()

#SQL Query3 - average steps by day of week 
query3 = """
SELECT day_of_week , AVG(steps) AS avg_steps
FROM health
GROUP BY day_of_week
ORDER BY avg_steps DESC
"""
health_df = pd.read_sql_query(query3, conn)
print(health_df)

fig3 = px.bar(
    health_df,
    x = 'day_of_week',
    y = "avg_steps",
    color = 'avg_steps',
    title = 'Average steps throughout the week'
)
fig3.show()

#SQL query4 - What muscle group has the most average volume per set and highest average rep per set
query4 = """
SELECT muscle_group , AVG(volume) AS avg_volume, AVG(reps) AS avg_reps
from lifting
GROUP BY muscle_group
ORDER BY avg_volume, avg_reps DESC
"""
muscle_df = pd.read_sql_query(query4, conn)
print(muscle_df)

fig4 = px.scatter(
    muscle_df,
    x = 'avg_volume',
    y = 'avg_reps',
    color = 'muscle_group',
    title = 'Average Volume and Reps per muscle group'
)
fig4.show()