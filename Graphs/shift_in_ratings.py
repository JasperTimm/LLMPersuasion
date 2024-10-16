import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch debate data
def get_debate_data(db_path):
    conn = sqlite3.connect(db_path)
    query = """
        SELECT initial_likert_score, final_likert_score 
        FROM debate 
        WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to calculate the absolute differences and group by difference
def calculate_differences(df):
    # Calculate the absolute difference between initial and final ratings
    df['difference'] = (df['initial_likert_score'] - df['final_likert_score']).abs()
    
    # Group by difference and count occurrences
    difference_counts = df['difference'].value_counts().sort_index()
    
    # Fill in missing difference values (0 to 6) with 0 counts
    all_differences = pd.Series(0, index=range(7))
    difference_counts = all_differences.add(difference_counts, fill_value=0).astype(int)
    
    return difference_counts

# Plot the graph using Streamlit and matplotlib
def plot_difference_chart(difference_counts):
    fig, ax = plt.subplots()
    ax.bar(difference_counts.index, difference_counts.values, color='skyblue')
    
    ax.set_xlabel("Absolute Difference in Ratings")
    ax.set_ylabel("Number of Debates")
    ax.set_title("Difference in Initial and Final Ratings by Number of People")
    
    # Display the plot
    st.pyplot(fig)

# Main function to run the Streamlit app
def main():
    st.title("Debate Rating Difference Visualization")
    
    # Path to your SQLite database
    db_path = 'debate_website_prod_latest.sqlite'  # Update with your actual database path
    
    # Load data from the database
    debate_data = get_debate_data(db_path)
    
    # Calculate the differences
    difference_counts = calculate_differences(debate_data)
    
    # Plot the graph
    plot_difference_chart(difference_counts)

# Run the Streamlit app
if __name__ == "__main__":
    main()
