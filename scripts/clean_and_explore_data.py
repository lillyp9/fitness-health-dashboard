import pandas as pd

#Create new DataFrames by loading the data from the CSV files
lifting_df = pd.read_csv('../data/lifting_data.csv')
health_df = pd.read_csv('../data/daily_health_metrics.csv')

#Print results
print("Data Loaded Successfully!")
print(f"Lifting rows: {len(lifting_df)}") #formatted string to print out the number of rows in the lifting DataFrame
print(f"Health rows: {len(health_df)}") #formatted string to print out the number of rows in the health DataFrame

#Preview Data 
print("\nLifting Data :")
print(lifting_df.head()) #prints the rows of the lifting DataFrame
print("\nHealth Data :")
print(health_df.head()) #prints the rows of the health DataFrame
#columns name 
print("\nLifting Columns:")
print(lifting_df.columns) #prints the column names of the lifting DataFrame
print("\nHealth Columns:")
print(health_df.columns) #prints the column names of the health DataFrame

#======Questions to Explore======
#1. How does the total weight lifted change over time?
total_weight_by_date = lifting_df.groupby('date')['volume'].sum() #groups the lifting data by date and sums the total weight lifted for each date
lifting_df['percentage_total'] = (lifting_df['volume'] / lifting_df['volume'].sum()) * 100 #calculates the mean of the total weight lifted by date
print(lifting_df[['exercise', 'percentage_total']].sort_values(by='percentage_total', ascending=False)) #sorts the lifting DataFrame by the percentage of total weight lifted in descending order
print("\nTotal Weight Lifted by Date:")
print(total_weight_by_date) #prints the total weight lifted by date
print("\nPercentage of Total Weight Lifted by Date:")
print(lifting_df['percentage_total']) #prints the percentage of total weight lifted by date

# 2 What is the relationship between sleep  and daily health metrics like heart rate and calories burned?
#BMR baseline - 1500 cals for an active adult 
#For every beat that is below abg restingheart rate(70), and 5 cals (lower Hr = more efficient which leads to higher base burn)

health_df['bmr_estimate'] = 1500 + (70 - health_df['resting_heart_rate']) * 5

#calorie burn column created 
health_df['calorie_burned'] = health_df['bmr_estimate'] + health_df['active_calories']
#daily calories per day 
daily_calories = health_df.groupby('day_of_week')['calorie_burned'].sum().reset_index()
print(daily_calories)

correlation = health_df[['sleep_hours', 'resting_heart_rate', 'active_calories']].corr() #calculates the correlation between sleep hours, heart rate, and calories burned in the health DataFrame
print("\nCorrelation between Sleep Hours, Heart Rate, and Calories Burned:")
print(correlation) #prints the correlation matrix

#3. Question 3 - Total volume per exercise 
volume_by_exercise = lifting_df.groupby("exercise")["volume"].sum()
volume_by_exercise = volume_by_exercise.sort_values(ascending=False)
print("\n Total Volume by Exercise:")
print(volume_by_exercise)
