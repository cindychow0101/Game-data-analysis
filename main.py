#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''Question 1: Data Manipulation'''
'''Clean data and convert to correct csv format'''
df = pd.read_csv("game_data.csv", delimiter='|')
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.columns = df.columns.str.replace(' ', '', regex=True).str.strip()
df = df.map(lambda x: x.replace(' ', '') if isinstance(x, str) else x)
df = df[~df.apply(lambda x: x.str.contains('^-+$').any(), axis=1)]
df.dropna(inplace=True)
df['timestamp'] = df['timestamp'].str.replace(r'(\d{4}-\d{2}-\d{2})(\d{2}:\d{2}:\d{2})', r'\1 \2', regex=True)
df.to_csv("cleaned_game_data.csv", index=False)

'''Categorize scores with new column'''
df['game_id'] = df['game_id'].astype(int)
df['player_id'] = df['player_id'].astype(int)
df['score'] = df['score'].astype(int)
df['level'] = df['level'].astype(int)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df["score_category"] = df["score"].apply(
    lambda x: 'Low' if x < 50 else ('Medium' if x >= 50 and x < 80 else 'High')
)
# print("Cleaned data:")
# print(df)

'''Group and calculate average scores by level'''
average_scores_by_level = df.groupby('level')['score'].mean().reset_index()
average_scores_by_level.index = average_scores_by_level.index + 1
# print("Average scores by level:")
# print(average_scores_by_level)

'''Question 2: Data Analysis'''
'''Find average score of players across all levels'''
average_score = df['score'].mean()
# print(f"Average score of players across all levels: {average_score}")

'''Find level which has the highest average score'''
highest_average_score_index = average_scores_by_level['score'].idxmax()
highest_average_score_level = average_scores_by_level.loc[highest_average_score_index]
# print(f"\nLevel {int(highest_average_score_level['level'])} with the highest average score of {highest_average_score_level['score']}")

'''Number of players scored in the High category'''
category_counts = df["score_category"].value_counts()
category_counts = category_counts.reindex(['High', 'Medium', 'Low'], fill_value=0)
# print(f"Number of players scored in the 'High' category: {category_counts['High']}")

'''Question 3: Data Visualization'''
'''Bar chart showing average score by level'''
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x='level', y='score', data=average_scores_by_level, palette='viridis', hue='level', legend=False)
plt.title('Average Scores by Level', fontsize=16, fontweight='bold')
plt.xlabel('Level', fontsize=14)
plt.ylabel('Average Score', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for p in bar_plot.patches:
    bar_plot.annotate(round(p.get_height(), 2), 
                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha='center', va='bottom', fontsize=10)
plt.tight_layout()

'''Pie chart showing score distribution by categories'''
plt.figure(figsize=(8, 6))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=['#FF9999', '#66B3FF', '#99FF99'])
plt.title('Score Distribution by Categories', fontsize=16, fontweight='bold')
plt.axis('equal')
# plt.show()

'''Question 4: Write a Function'''
def view_player():
    selected_player = input("Enter player ID: ").strip()

    try:
        selected_player = int(selected_player)
        if selected_player not in df['player_id'].values:
            print("No player found with that ID.")
            return
        
        filtered_df = df[df['player_id'] == selected_player]

        highest_score_index = filtered_df['score'].idxmax()
        highest_score = filtered_df.loc[highest_score_index, 'score']
        corresponding_level = filtered_df.loc[highest_score_index, 'level']
        
        print(f"Player {selected_player} achieved highest score of {highest_score} at level {corresponding_level}.")
    
    except ValueError:
        print("Please enter a valid player ID.")

# view_player()

'''View the answer of each question by running the file and entering question number.'''
def show_answer():
    while True:
        print("\nTo view answer: ")
        choice = input("Enter the question number (Leave it empty to exit the loop): ").strip()
    
        if choice == "1":
            print("Question 1 Answer")
            print("Cleaned data:")
            print(df)
            print("Average scores by level:")
            print(average_scores_by_level)
        
        elif choice == "2":
            print("\nQuestion 2 Answer")
            print(f"Average score of players across all levels: {average_score}")
            print(f"Level {int(highest_average_score_level['level'])} with the highest average score of {highest_average_score_level['score']}")
            print(f"Number of players scored in the 'High' category: {category_counts['High']}")
            
        elif choice == "3":
            print("\nQuestion 3 Answer")
            plt.show()
        
        elif choice == "4":
            print("\nQuestion 4 Answer")
            print("Test the function by inputting player ID.")
            view_player()
            
        elif choice == "":
            print("\nExiting...")
            break
        
        else:
            print("\nPlease enter a valid number.")
            
show_answer()
# %%