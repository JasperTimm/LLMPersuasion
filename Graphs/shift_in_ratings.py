import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch debate data with pre-calculated rating differences
def get_debate_data(db_path):
    conn = sqlite3.connect(db_path)
    query = """
        SELECT rating_difference 
        FROM debate 
        WHERE rating_difference IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to group by rating difference and count occurrences
def calculate_differences(df):
    # Group by difference and count occurrences
    difference_counts = df['rating_difference'].value_counts().sort_index()

    # Assuming the range of possible rating differences (-6 to 6), fill in missing values with 0 counts
    all_differences = pd.Series(0, index=range(-6, 7))  # Includes negative values
    difference_counts = all_differences.add(difference_counts, fill_value=0).astype(int)
    
    return difference_counts

# Plot the graph using Streamlit and matplotlib
def plot_difference_chart(difference_counts):
    fig, ax = plt.subplots()
    ax.bar(difference_counts.index, difference_counts.values, color='skyblue')
    
    ax.set_xlabel("Rating Difference (Negative to Positive)")
    ax.set_ylabel("Number of Debates")
    ax.set_title("Distribution of Rating Differences (Initial vs. Final)")

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
