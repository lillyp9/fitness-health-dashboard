import pandas as pd
import sqlite3
import plotly.express as px
from dash import Dash, dcc, html, Input, Output 

#initalizing app
app = Dash(__name__)

#server to run 
server = app.server 

conn = sqlite3.connect("data/fitness.db")

#====================== SQL QUERY 1 : Total volume by exercise
query = """
SELECT exercise, SUM(volume) AS total_volume
FROM lifting
GROUP BY exercise
ORDER BY total_volume DESC
"""
#print out table 
volume_df = pd.read_sql_query(query, conn)
print(volume_df)
#total sets pulls from lifting 
sets_query = """
SELECT COUNT(*) AS total_sets FROM lifting
"""
#print out the sets 
sets_stats = pd.read_sql_query(sets_query, conn)

#============== HORIZONTAL CHART
fig1 = px.bar( #create bar chart
    volume_df, #dataframe 
    x = "total_volume", # column
    y = "exercise", #column
    orientation = "h", #horizontal 
    title = "Total Volume by Exercise", 
    labels = {"total_volume": "Total volume(lbs x reps)", "exercise": "Exercise"},
    color = "total_volume",#automatic color bars by value , darker = higher
    template="plotly_dark"
)

#======================== SQL Query2 - weekly progression
query2 = """
SELECT exercise, date, AVG(weight_lbs) as avg_weight
FROM lifting
GROUP BY exercise, date
ORDER BY exercise, date
"""
#print out table 
progression_df = pd.read_sql_query(query2, conn)
print(progression_df)

#============= LINE CHART

fig2 = px.line(
    progression_df,
    x = "date",
    y = "avg_weight",
    color = "exercise",
    title = "Average Weight By Exercise Over Time",
    template="plotly_dark"
) 


# =============================== SQL Query3 - average steps by day of week 
query3 = """
SELECT day_of_week , AVG(steps) AS avg_steps
FROM health
GROUP BY day_of_week
ORDER BY avg_steps DESC
"""
health_df = pd.read_sql_query(query3, conn)
print(health_df)
#part of query3 - motnh filter 
monthly_query = """
SELECT day_of_week, month, AVG(steps) As avg_steps
FROM health
GROUP BY month, day_of_week
Order BY avg_steps DESC
"""
monthly_df = pd.read_sql_query(monthly_query, conn)

#sperate health query that pulls actual sleep 
sleep_query ="""
SELECT AVG(sleep_hours) AS avg_sleep, AVG(resting_heart_rate) AS avg_rhr
FROM health
"""
sleep_stats = pd.read_sql_query(sleep_query, conn)

#==================== CHART 3
fig3 = px.bar(
    health_df,
    x = 'day_of_week',
    y = "avg_steps",
    color = 'avg_steps',
    title = 'Average steps throughout the week',
    template="plotly_dark"
)


#============================ SQL query4 - What muscle group has the most average volume per set and highest average rep per set
query4 = """
SELECT muscle_group , AVG(volume) AS avg_volume, AVG(reps) AS avg_reps
from lifting
GROUP BY muscle_group
ORDER BY avg_volume, avg_reps DESC
"""
muscle_df = pd.read_sql_query(query4, conn)
print(muscle_df)

# =========================== CHART 4
fig4 = px.scatter(
    muscle_df,
    x = 'avg_volume',
    y = 'avg_reps',
    color = 'muscle_group',
    title = 'Average Volume and Reps per muscle group',
    template="plotly_dark"
)

#============================ CHART 5 (Sleep vs Resting Heart Rate) 
trend_query = """
SELECT date, sleep_hours, resting_heart_rate, steps, month 
FROM health 
ORDER BY date 
"""
trend_df = pd.read_sql_query(trend_query, conn)
print(trend_df)

#============================= SCATTER PLOT 
fig5 = px.scatter(
    trend_df,
    x = "sleep_hours",
    y = "resting_heart_rate",
    color = "month",
    title = "Sleep vs Resting Heart Rate",
    template = "plotly_dark",
    labels = {"sleep_hours": "Sleep (hrs)", "resting_heart_rate":"Resting HR (bpm)"}
    
)

#========================= CHART 6 (Total steps per month)
monthly_steps_query = """
SELECT month , SUM(steps) AS total_steps
FROM health 
GROUP BY month
ORDER BY total_steps DESC
"""
monthly_steps_df = pd.read_sql_query(monthly_steps_query, conn)
print(monthly_steps_df)

#============================ BAR CHART 
fig6 = px.bar(
    monthly_steps_df,
    x = "month",
    y = "total_steps",
    color = "month",
    title = "Total of steps throughout the months",
    template = "plotly_dark",
    labels = {"total_steps": "Total Steps", "month": "Month" }
)

#======= App Layout =============
app.layout = html.Div(style={"backgroundColor":"#111111", "fontFamily": "Arial", "padding": "20px"}, children=[
    #Title - Heading
    html.H1("Fitness Health Dashboard", 
        style={"textAlign": "center", "color": "#00d4ff", "marginBottom": "10px"}),
    html.P("Tracking lifitng progress , daily activity, and helath metrics",
        style={"textAlign": "center","color": "#aaaaaa", "marginBottom":"30px"}),
#===================================================== CARDS ====================================
#--------------------CARD 1 - Total Sets  -----------
html.Div(style={"display": "flex", "justifyContent": "space-around", "marginBottom": "40px"}, children=[
    html.Div(style={"backgroundColor": "#1e1e1e", "padding": "20px", "borderRadius":"10px",
                    "textAlign": "center", "width": "20%", "border": "1px solid #00d4ff"}, children=[
        html.H3("Total Sets", style={"color": "#aaaaaa", "fontSize": "14px"}),
        html.H2(f"{sets_stats['total_sets'].iloc[0]}",
            style={"color": "#00d4ff", "fontSize": "32px"}),
]),
#---------------------CARD 2 - Avg Daily Steps ---------------------    
    html.Div(style={"backgroundColor": "#1e1e1e", "padding": "20px", "borderRadius": "10px",
                "textAlign":"center", "width": "20%", "border": "1px solid #00d4ff"}, children=[
        html.H3("Avg Daily Steps", style={"color": "#aaaaaa", "fontSize": "14px"}),
        html.H2(f"{health_df['avg_steps'].mean():,.0f}", style={"color": "#00ff99", "fontSize": "32px"}),     
    ]),
#--------------------CARD 3 -Avg Sleep -----------------
    html.Div(style={"backgroundColor": "#1e1e1e", "padding": "20px", "borderRadius": "10px",
                    "textAlign": "center", "width": "20%", "border": "1px solid #ff6b6b"}, children=[
        html.H3("Avg Sleep", style={"color": "#aaaaaa", "fontSize": "14px"}),
        html.H2(f"{sleep_stats['avg_sleep'].iloc[0]:.1f} hrs",
            style={"color": "#ff6b6b", "fontSize": "32px"}),
    ]),
#--------------CARD 4 -Avg Resting Heart Rate  -------------------------         
html.Div(style={"backgroundColor": "#1e1e1e", "padding": "20px", "borderRadius": "10px",
                    "textAlign": "center", "width": "20%", "border": "1px solid #ffaa00"}, children=[
        html.H3("Avg Resting HR", style={"color": "#aaaaaa", "fontSize": "14px"}),
        html.H2(f"{sleep_stats['avg_rhr'].iloc[0]:.1f} bpm",
                style={"color": "#ffaa00", "fontSize": "32px"}),
    ]),
]),                             
#============================== Charts ==================  
    #============== Chart 1 
    html.H2("Total Volume by Exercise",
        style={"color": "#ffffff", "borderBottom": "1px solid #333333", "paddingBottom": "10px"}),   
    dcc.Graph(figure=fig1),
    #===============  Chart 2 
    html.H2("Weekly Progression",
        style={"color": "#ffffff", "borderBottom": "1px solid #333333", "paddingBottom": "10px"}),
    #dropdown filter 
    dcc.Dropdown(
        id="exercise-dropdown", #dropdown name so callback can find 
        options=[{"label": ex, "value": ex} for ex in progression_df["exercise"].unique()], # build list from data 
        value = None,
        placeholder= "Filter by exercise", 
        multi = True, #function lets user pick more then just one exercise
        style = {"backgroundColor": "#1e1e1e", "color": "#000000", "marginBottom": "20px"}
    ),
    
    dcc.Graph(id="progression-chart"), # chart name so callback can update 
    
    #==========================  Chart 3 
    html.H2("Average Steps by Day of Week",
        style={"color": "#ffffff", "borderBottom": "1px solid #333333", "paddingBottom": "10px"}),   
    #dropdwon feature 
    dcc.Dropdown(
        id="monthly-dropdown", #dropdown name sp call back can find 
        options=[{"label": m, "value": m} for m in monthly_df["month"].unique()],
        value=None,
        placeholder="Filter by month",
        multi = True,
        style={"backgroundColor": "#1e1e1e", "color": "#000000", "marginBottom": "20px"}
    ),
    
    dcc.Graph(id = "steps-chart"), #chart name so call back can find  
    
    #===========================   Chart 4
    html.H2("Volume vs Reps by Muscle Group",
          style={"color": "#ffffff", "borderBottom": "1px solid #333333", "paddingBottom": "10px"}), 
      
    dcc.Graph(figure=fig4),

    #=========================  Chart 5
    html.H2("Sleep vs Resting Heart Rate",
        style={"color": "#ffffff", "borderBottom": "1px solid #333333", "paddingBottom": "10px"}),
    dcc.Graph(figure=fig5),

    #======================== Chart 6
    html.H2("Monthly Steps Trend",
        style={"color": "#ffffff", "borderBottom": "1px solid #333333", "paddingBottom": "10px"}),
    dcc.Graph(figure=fig6),
])

# =========== CALLBACK FOR CHART 2 ==============
@app.callback( #function runs when soemhting chnages 
    Output("progression-chart", "figure"), #chart that gets updated 
    Input("exercise-dropdown", "value") #trigger the update 
)
def update_progression(selected_exercises): #update the progression by selected exercise 
    if not selected_exercises: #if nothing selected , show all exercise 
        filtered_df = progression_df #filter data is equal to progressions data 
    else: #filter data based on what the user picks 
        filtered_df = progression_df[progression_df["exercise"].isin(selected_exercises)]

    fig = px.line(
        filtered_df,
        x="date",
        y="avg_weight",
        color="exercise",
        title="Weekly Progression by Exercise",
        template="plotly_dark",
        labels={"avg_weight": "Avg Weight (lbs)", "date": "Date"}
    )
    return fig #send the new chart to dashboard 

# ============ CALLBACK CHART 3 =============
@app.callback(
    Output("steps-chart", "figure"),
    Input("monthly-dropdown", "value")
)
def update_steps(selected_months):
    if not selected_months:
       filtered_df = monthly_df
    else:
        filtered_df = monthly_df[monthly_df["month"].isin(selected_months)]

    fig = px.bar(
        filtered_df,
        x="day_of_week",
        y="avg_steps",
        color="month",
        barmode="group", #if multiple months selected bars are side by side , to better compare 
        title="Avg Steps by Day of Week",
        template="plotly_dark",
        labels={"avg_steps": "Avg Steps", "day_of_week": "Day"}
    )
    return fig     #send new chart to dashboard 

#run app
if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=8050
            )