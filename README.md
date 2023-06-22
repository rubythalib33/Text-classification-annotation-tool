# Sentiment Analysis Annotation Tool

This tool is designed to facilitate sentiment analysis annotation tasks. It provides the following features:

- Annotation with auto-annotation: You can manually annotate sentiment labels for text data. Additionally, there is an option for auto-annotation that automatically assigns sentiment labels based on a pre-trained model.
- Generate Data: You can generate synthetic data for sentiment analysis tasks.
- Auto EDA (still in development): Automatic Exploratory Data Analysis (EDA) functionality is being developed to provide insights and visualizations for the annotated data.

## Setup

1. Clone the repository:

   ```shell
   git clone https://github.com/rubythalib33/Text-classification-annotation-tool
   ```
2. Navigate to the project directory:
    ```shell
    cd Text-classification-annotation-tool
    ```
3. install the requirements
    ```shell
    pip install -r requirements
    ```
4. Create a .env file in the project directory and add the following line, replacing <YOUR_OPENAI_API_KEY> with your actual OpenAI API key:
    ```shell
    OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
    ```

## How to run
To start the application, run the following command:
```shell
streamlit run app.py
```

hope this project help you..