import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# Database connection
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///instance/debate_website_prod.sqlite')
engine = create_engine(DATABASE_URI)

def fetch_data(query):
    """Fetch data from the database using the provided SQL query."""
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

def plot_scatter(df, x_col, y_col, title='Graph', xlabel='X-axis', ylabel='Y-axis'):
    """Plot scatter data using seaborn."""
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    st.pyplot(plt)

def plot_bar_graph(df, x_col, title='Graph', xlabel='X-axis', ylabel='Y-axis'):
    """Plot bar graph using seaborn."""
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=x_col)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    st.pyplot(plt)

def scatter_plot_interface():
    """Streamlit interface for scatter plot."""
    st.title('Debate Opinion Analysis - Scatter Plot')

    # Query to fetch initial and final opinions
    query = """
    SELECT initial_likert_score, final_likert_score
    FROM debate
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL
    """

    # Fetch data
    df = fetch_data(query)

    # Calculate deltas in opinion
    df['opinion_delta'] = df['final_likert_score'] - df['initial_likert_score']

    # Streamlit interface for selecting columns and filters
    x_col = st.selectbox('Select X-axis column', df.columns)
    y_col = st.selectbox('Select Y-axis column', df.columns)
    title = st.text_input('Graph Title', 'Opinion Delta Scatterplot')
    xlabel = st.text_input('X-axis Label', x_col)
    ylabel = st.text_input('Y-axis Label', y_col)

    # Plot data
    plot_scatter(df, x_col=x_col, y_col=y_col, title=title, xlabel=xlabel, ylabel=ylabel)

def bar_graph_interface():
    """Streamlit interface for bar graph."""
    st.title('Debate Opinion Analysis - Bar Graph')

    # Query to fetch initial and final opinions along with debate type
    query = """
    SELECT initial_likert_score, final_likert_score, llm_debate_type
    FROM debate
    WHERE initial_likert_score IS NOT NULL AND final_likert_score IS NOT NULL
    """

    # Fetch data
    df = fetch_data(query)

    # Calculate deltas in opinion
    df['opinion_delta'] = df['final_likert_score'] - df['initial_likert_score']

    # Streamlit dropdown for selecting debate type
    debate_types = df['llm_debate_type'].unique()
    selected_debate_type = st.selectbox('Select Debate Type', debate_types)

    # Filter data based on selected debate type
    filtered_df = df[df['llm_debate_type'] == selected_debate_type]

    # Plot bar graph
    plot_bar_graph(filtered_df, x_col='opinion_delta', title=f'Opinion Delta for {selected_debate_type} Debates', xlabel='Opinion Delta', ylabel='Count')

if __name__ == "__main__":
    scatter_plot_interface()
    bar_graph_interface()