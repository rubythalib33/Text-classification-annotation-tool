import streamlit as st
import pandas as pd
import os
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from engine import sentiment_analysis, generate_data, extract_generated_data


st.set_option('deprecation.showPyplotGlobalUse', False)

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
    df = pd.read_csv("data/data.csv")

    # bar chart of balance of the data
    st.markdown("### Balance of the data")
    st.bar_chart(df["sentiment"].value_counts())

    # word length distribution
    st.markdown("### Word Length Distribution")
    df["word_length"] = df["text"].apply(lambda x: len(x.split(" ")))
    st.bar_chart(df["word_length"].value_counts())

    sentiment_options = ["negative", "neutral", "positive"]
    selected_sentiment = st.selectbox("Select Sentiment", sentiment_options)
    df_selected = df[df["sentiment"] == selected_sentiment]

    # word cloud
    st.markdown("### Word Cloud")
    wordcloud = WordCloud().generate(' '.join(df_selected["text"]))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

    # word frequency on each sentiment
    st.markdown("### Word Frequency")

    frequency = {}
    for text in df_selected["text"]:
        for word in text.split(" "):
            if word not in frequency:
                frequency[word] = 1
            else:
                frequency[word] += 1
    df_frequency = pd.DataFrame.from_dict(frequency, orient='index', columns=['frequency'])
    df_frequency = df_frequency.sort_values(by=['frequency'], ascending=False)
    st.bar_chart(df_frequency.head(10))

    # bigram
    st.markdown("### Bigram")
    bigram_frequency = {}
    for text in df_selected["text"]:
        text = text.split(" ")
        for i in range(len(text)-1):
            bigram = text[i] + " " + text[i+1]
            if bigram not in bigram_frequency:
                bigram_frequency[bigram] = 1
            else:
                bigram_frequency[bigram] += 1
    df_bigram_frequency = pd.DataFrame.from_dict(bigram_frequency, orient='index', columns=['frequency'])
    df_bigram_frequency = df_bigram_frequency.sort_values(by=['frequency'], ascending=False)
    st.bar_chart(df_bigram_frequency.head(10))

    # trigram
    st.markdown("### Trigram")
    trigram_frequency = {}
    for text in df_selected["text"]:
        text = text.split(" ")
        for i in range(len(text)-2):
            trigram = text[i] + " " + text[i+1] + " " + text[i+2]
            if trigram not in trigram_frequency:
                trigram_frequency[trigram] = 1
            else:
                trigram_frequency[trigram] += 1
    df_trigram_frequency = pd.DataFrame.from_dict(trigram_frequency, orient='index', columns=['frequency'])
    df_trigram_frequency = df_trigram_frequency.sort_values(by=['frequency'], ascending=False)
    st.bar_chart(df_trigram_frequency.head(10))

# Render the View All Data page
def render_view_all_data():
    st.header("View All Data Page")
    try:
        df = pd.read_csv("data/data.csv")
        st.write(df)

        # Add download button
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
    except:
        st.write("No data found plase provide the data inside data folder with data.csv format with header id,text,sentiment or you can do it with generate data feature")

    