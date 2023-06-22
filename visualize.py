import streamlit as st
import pandas as pd
import os

from engine import sentiment_analysis, generate_data, extract_generated_data

# Render the header
def render_header():
    st.title("Sentiment Analysis Annotation tool")
    st.write("---")

# Render the Annotation page
def render_annotation():
    st.header("Annotation Page")

    df = pd.read_csv("data/data.csv")

    # Add input options for selecting ID or new data generation
    input_options = ["Select ID", "Generate New Data"]
    input_selection = st.radio("Select Input Option", input_options)

    sentiment_options = ["negative", "neutral", "positive"]

    # If "Select ID" is chosen, show selectbox to choose ID
    if input_selection == "Select ID":
        # Get a list of available IDs (replace with your own logic)
        available_ids = df["id"].unique().tolist()

        selected_id = st.selectbox("Select ID", available_ids)
        # Logic to fetch the data corresponding to the selected ID and display it
        new_data_text = st.text_area("Text", value=df[df["id"] == selected_id]["text"].values[0], height=100)
        selected_sentiment = st.selectbox("Select Sentiment", sentiment_options, index=sentiment_options.index(df[df["id"] == selected_id]["sentiment"].values[0]))

    # If "Generate New Data" is chosen, show text area and sentiment selection
    else:
        new_data_text = st.text_area("Text")
        if new_data_text:
            annotation_result = sentiment_analysis(new_data_text).lower()
            selected_sentiment = st.selectbox("Select Sentiment", sentiment_options, index=sentiment_options.index(annotation_result))

    # Add a button to save the data
    if st.button("Save"):
        # Logic to save the data (replace with your own logic)
        if input_selection == "Select ID":
            df.loc[df["id"] == selected_id, "text"] = new_data_text
            df.loc[df["id"] == selected_id, "sentiment"] = selected_sentiment
        else:
            new_id = df["id"].max() + 1
            new_row = {"id": new_id, "text": new_data_text, "sentiment": selected_sentiment}
            df = df.append(new_row, ignore_index=True)
        df.to_csv("data/data.csv", index=False)
        st.success("Data saved successfully")

# Render the Generate Data page
def render_generate_data():
    st.header("Generate Data Page")
    # Add your data generation logic here

    col1, col2, col3 = st.columns(3)
    
    with col1:
        n_data = st.number_input("Number of data", value=5)
    with col2:
        type_text = st.selectbox("Type of text", ["short", "long", "paragraph"])
    with col3:
        sentiment = st.selectbox("Sentiment", ["positive", "negative", "neutral"])

    df_new = None
    if st.button("Generate"):
        output = generate_data(n_data, type_text, sentiment)
        result = extract_generated_data(output)
        df_new = pd.DataFrame(result)
        st.write(df_new)
        if os.path.exists("data/data.csv"):
            df_old = pd.read_csv("data/data.csv")
            # add id
            df_old_max_id = df_old["id"].max()
            df_new["id"] = range(df_old_max_id+1, df_old_max_id+1+len(df_new))
            df_new = pd.concat([df_old, df_new], ignore_index=True)
            df_new.to_csv("data/data.csv", index=False)
        else:
            df_new["id"] = range(1, len(df_new)+1)
            df_new.to_csv("data/data.csv", index=False)
        st.success("Data saved successfully")

# Render the EDA page
def render_eda():
    st.header("EDA Page")
    # Add your exploratory data analysis logic here

# Render the View All Data page
def render_view_all_data():
    st.header("View All Data Page")
    try:
        df = pd.read_csv("data/data.csv")
        st.write(df)
    except:
        st.write("No data found plase provide the data inside data folder with data.csv format with header id,text,sentiment")
    